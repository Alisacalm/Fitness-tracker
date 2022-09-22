from dataclasses import dataclass, asdict
from typing import Sequence, Type, Dict, Tuple, Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration_hrs: float = duration
        self.weight_kg: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_hrs

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('В дочернем классе должен быть определен '
                                  'метод get_spent_calories.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration_hrs,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLIER_CALORY: int = 18
    SPEED_DIFF_CALORY: int = 20

    def get_spent_calories(self) -> float:
        return ((self.SPEED_MULTIPLIER_CALORY * self.get_mean_speed()
                 - self.SPEED_DIFF_CALORY) * self.weight_kg / self.M_IN_KM
                * self.duration_hrs * self.MIN_IN_HR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER_CALORY: float = 0.035
    SPEED_CALORY_MULTIPLIER: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        return ((self.WEIGHT_MULTIPLIER_CALORY * self.weight_kg
                 + (self.get_mean_speed()**2
                    // self.height_cm) * self.SPEED_CALORY_MULTIPLIER
                 * self.weight_kg)
                * (self.duration_hrs * self.MIN_IN_HR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SPEED_SWIM_CALORY: float = 1.1
    WEIGHT_CALORY_MULTIPLIER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool_m * self.count_pool
                / self.M_IN_KM / self.duration_hrs)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SPEED_SWIM_CALORY)
                * self.WEIGHT_CALORY_MULTIPLIER * self.weight_kg)


def read_package(workout_type: str, data: Union[int, float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking,
                                                }
    if workout_type in training_type:
        return (training_type[workout_type](*data))
    raise ValueError(f'Неизвестный тип тренировки:{workout_type}. '
                     'Доступны следующие типы тренировок:{training_type}.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: Sequence[Tuple[str, Union[int, float]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]), ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)