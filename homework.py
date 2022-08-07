from dataclasses import dataclass
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    action: int
    duration: float
    weight: float
    CONVERT_TO_MINUTES: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Ошибка в классе {type(self).__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIE_CALC_COEFICENT_FOR_RUNNING_1: float = 18
    CALORIE_CALC_COEFICENT_FOR_RUNNING_2: float = 20

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIE_CALC_COEFICENT_FOR_RUNNING_1 * self.get_mean_speed()
             - self.CALORIE_CALC_COEFICENT_FOR_RUNNING_2)
            * self.weight / self.M_IN_KM
            * (self.duration * self.CONVERT_TO_MINUTES)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    CALORIE_CALC_COEFICENT_FOR_WALK_1: float = 0.035
    CALORIE_CALC_COEFICENT_FOR_WALK_2: float = 2
    CALORIE_CALC_COEFICENT_FOR_WALK_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIE_CALC_COEFICENT_FOR_WALK_1 * self.weight
             + (self.get_mean_speed()**self.CALORIE_CALC_COEFICENT_FOR_WALK_2
                // self.height)
             * self.CALORIE_CALC_COEFICENT_FOR_WALK_3 * self.weight)
            * (self.duration * self.CONVERT_TO_MINUTES)
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    length_pool: float
    count_pool: int
    CALORIE_COUNTING_COEFFICIENT_FOR_SWIMMING_1: float = 1.1
    CALORIE_COUNTING_COEFFICIENT_FOR_SWIMMING_2: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed()
             + self.CALORIE_COUNTING_COEFFICIENT_FOR_SWIMMING_1)
            * self.CALORIE_COUNTING_COEFFICIENT_FOR_SWIMMING_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Type[Training]:
    """Прочитать данные полученные от датчиков."""
    training_type = {'RUN': Running,
                     'SWM': Swimming,
                     'WLK': SportsWalking}
    if workout_type not in training_type:
        raise KeyError(
            f'Тренировки {workout_type} не существует'
        )
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)