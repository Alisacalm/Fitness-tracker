from typing import Sequence, Type, Dict, Tuple, List


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; ' 
                f'Длительность: {self.duration:.3f} ч.; ' 
                f'Дистанция: {self.distance:.3f} км; ' 
                f'Ср. скорость: {self.speed:.3f} км/ч; ' 
                f'Потрачено ккал: {self.calories:.3f}.')


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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    run_calorie_1 = 18
    run_calorie_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.run_calorie_1 * self.get_mean_speed() 
                - self.run_calorie_2) * self.weight / self.M_IN_KM 
                * self.duration * self.MIN_IN_HR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    walk_calorie_1 = 0.035
    walk_calorie_2 = 0.029
    speed_coeff = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self) -> float:
        return ((self.walk_calorie_1 * self.weight 
                + (self.get_mean_speed()**self.speed_coeff 
                // self.height) * self.walk_calorie_2 * self.weight) 
                * (self.duration * self.MIN_IN_HR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    swim_calorie = 1.1
    coeff_calorie = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool 
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.swim_calorie) 
                * self.coeff_calorie * self.weight) 

def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking,
                                                }
    if workout_type in training_type:
        return (training_type[workout_type](*data))
    raise ValueError("Неизвестный тип тренировки.")

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())

if __name__ == '__main__':
    packages: Sequence[Tuple[str, List[int]]] = [('SWM', [720, 1, 80, 25, 40]),
                                                 ('RUN', [15000, 1, 75]),
                                                 ('WLK', [9000, 1, 75, 180]),
                                                 ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)