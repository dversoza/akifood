class Base:
    def __init__(self) -> None:
        pass


class Dishes(Base):
    def __init__(self) -> None:
        super().__init__()
        pass


class Adjectives(Base):
    def __init__(self) -> None:
        super().__init__()
        pass


class Relationships(Base):
    def __init__(self) -> None:
        super().__init__()
        pass


db: list = []

if __name__ == '__main__':
    """Program entry point"""
    print('App running')
