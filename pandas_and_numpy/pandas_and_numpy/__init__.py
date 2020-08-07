import pandas as pd
import numpy as np

df = pd.DataFrame({
    'x': [0, 1, 0, 1, 0, 1, 0, 1],
    'y': [7, 6, 5, 4, 3, 2, 1, 0],
    'number': np.random.randn(8),
})

def field_name_prettifier(newname):
    def decorator(f):
        f.__name__ = newname
        return f
    return decorator

def q_at(y):
    @field_name_prettifier(f'q{y:0.2f}')
    def q(x):
        return x.quantile(y)
    return q

def main(**kwargs):
    return df \
        .groupby('x') \
        .agg({
            'number': ['median', 'std', q_at(0.25), q_at(0.75), q_at(0.95)]
        }) \
        .to_json(orient='split', force_ascii=False)

if __name__ == "__main__":
    print(f"{main()}")
