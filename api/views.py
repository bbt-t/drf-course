from django.http import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Course, Lesson, Payment
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (
    CourseSerializer,
    UserSerializer,
    LessonSerializer,
    PaymentSerializer,
)
from auth_api.models import Student


class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


# class PaymentListAPIView(generics.ListAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     filter_backends = [OrderingFilter, DjangoFilterBackend]
#     filterset_fields = "course", "lesson", "payment_method"
#     ordering_fields = ("pay_date",)
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PaymentListAPIView(ListAPIView):
    """
    Представление для отображения списка платежей.

    Менеджеры могут видеть весь список, обычные юзеры - только свои платежи
    """

    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('course', 'way_pay')
    ordering_fields = ('date',)
    permission_classes = [IsAuthenticated]
    action = 'list'

    def get_queryset(self):
        if not self.request.user.groups.filter(name='Managers').exists():
            self.queryset = Payment.objects.filter(user=self.request.user)
        else:
            self.queryset = Payment.objects.all()
        queryset = super().get_queryset()

        return queryset


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscribe_to_updates(request: HttpRequest, pk: int) -> Response:
    """
    Представление для осуществления подписки на обновления курса или отмены подписки.
    Запрещено неавторизованным пользователям
    """

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Такой курс не существует."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if Subscription.objects.filter(course=course, user=request.user).exists():
            Subscription.objects.filter(course=course, user=request.user).delete()
            return Response({'message': f'Подписка на обновления курса {course.name} отменена!'},
                            status=status.HTTP_200_OK)

        data = {'course': pk, 'user': request.user.id}
        serializer = SubscriptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'Подписан на обновления курса {course.name}!'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pay_course(request: HttpRequest, course_pk: int) -> Response:
    """
    Представление для получения ссылки оплаты за курс, сразу перенаправляет на создание платежа
    Права доступа по умолчанию - только для авторизованных пользователей
    """

    try:
        course = Course.objects.get(pk=course_pk)
        if course:
            data = {
                'amount': course.price,
                'user': request.user.pk,
                'course': course.pk,
            }
            serializer = PaymentSerializer(data=data)
            if serializer.is_valid():
                payment = serializer.save()

                session_id, payment_url = services.get_payment_link(request, course, payment.pk)
                payment.id_stripe_session = session_id
                payment.save()

                # return HttpResponseRedirect(payment_url)
                return Response({"payment_url": payment_url}, status=status.HTTP_200_OK)
    except requests.RequestException:
        return Response({"error": "Ошибка доступа к сайту оплаты"}, status=status.HTTP_400_BAD_REQUEST)
    except Course.DoesNotExist:
        return Response({"error": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_payment(request: HttpRequest, payment_pk: int) -> Response:
    """
    Представление для проверки успешности платежа
    Права доступа - только для авторизованных пользователей
    """

    payment = Payment.objects.filter(pk=payment_pk).first()
    if payment and services.is_payment_succeed(payment.id_stripe_session):
        payment.is_succeed = True
        payment.save()
        return Response({'message': f'Оплачен курс {payment.course.name}!'},
                        status=status.HTTP_200_OK)
    return Response({'message': f'Курс {payment.course.name} не был оплачен!'},
                    status=status.HTTP_200_OK)


