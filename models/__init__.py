# from .producto_model import Producto
# from .carrito_model import Carrito
# from .usuario_model import Usuario
# from database import db
# #from flask_sqlalchemy import SQLAlchemy

# #db = SQLAlchemy()
# models/__init__.py
# ❌ Evita esto:
# from .usuario_model import Usuario
# from .producto_model import Producto
# from .carrito_model import Carrito

# ✅ Déjalo vacío o solo exporta `db` si quieres:
from database import db
