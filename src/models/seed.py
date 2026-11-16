from src.models import Session
from src.models.categories import Categories


def seed_categories():
    categories = [
        Categories(name="Medicamentos", description="Productos farmacéuticos", active=1),
        Categories(name="Cuidado personal", description="Productos de cuidado personal", active=1),
        Categories(name="Vitaminas", description="Vitaminas y suplementos", active=1),
    ]

    try:
        session = Session()
        session.add_all(categories)
        session.commit()
        print("Categorías iniciales creadas correctamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al crear las categorías: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_categories()