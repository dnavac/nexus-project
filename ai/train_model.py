import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Generamos datos ficticios de entrenamiento
# Features: [presupuesto_millones, num_visitas, dias_desde_contacto, responde_rapido(0/1)]
np.random.seed(42)
n_samples = 1000

X = np.column_stack([
    np.random.randint(100, 2000, n_samples),   # presupuesto en millones COP
    np.random.randint(0, 10, n_samples),         # número de visitas realizadas
    np.random.randint(1, 90, n_samples),         # días desde primer contacto
    np.random.randint(0, 2, n_samples),          # responde rápido (1=sí, 0=no)
])
# Regla simulada: compra si tiene buen presupuesto, varias visitas, pocos días y responde rápido
y = (
    (X[:, 0] > 300) &     # presupuesto > 300M
    (X[:, 1] >= 2) &       # al menos 2 visitas
    (X[:, 2] < 60) &       # menos de 60 días
    (X[:, 3] == 1)          # responde rápido
).astype(int)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
joblib.dump(model, "lead_model.joblib")
print("Modelo entrenado y guardado en lead_model.joblib")