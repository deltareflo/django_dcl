import pandas as pd
from .models import DatosPersonales, Disc, TrabajoEquipo, Liderazgo

def load_personal_data(id):
    """Loads all personal data into a DataFrame."""
    data = DatosPersonales.objects.filter(id=id).values()
    return pd.DataFrame(list(data))

def load_disc_data(id):
    """Loads DISC test data, reordering 'item_' fields and placing 'campo_unico' first."""
    disc_data = Disc.objects.filter(campo_unico=id).values()
    df_disc = pd.DataFrame(list(disc_data))

    if not df_disc.empty:
        # Identify 'item_' columns and sort them numerically
        item_cols = sorted([col for col in df_disc.columns if col.startswith('item_')],
                           key=lambda x: int(x.split('_')[1]))
        
        # Define the desired column order
        other_cols = [col for col in df_disc.columns if col not in ['campo_unico'] + item_cols]
        new_order = ['campo_unico'] + item_cols + other_cols
        
        # Filter out columns that don't exist in the DataFrame
        new_order = [col for col in new_order if col in df_disc.columns]
        
        df_disc = df_disc[new_order]
    return df_disc

def load_teamwork_data(id):
    """Loads Teamwork test data, placing 'campo_unico' first and then 'item_' fields."""
    teamwork_data = TrabajoEquipo.objects.filter(campo_unico=id).values()
    df_teamwork = pd.DataFrame(list(teamwork_data))

    if not df_teamwork.empty:
        item_cols = [col for col in df_teamwork.columns if col.startswith('item_')]
        other_cols = [col for col in df_teamwork.columns if col not in ['campo_unico'] + item_cols]
        new_order = ['campo_unico'] + item_cols + other_cols
        new_order = [col for col in new_order if col in df_teamwork.columns]
        df_teamwork = df_teamwork[new_order]
    return df_teamwork

def load_leadership_data(id):
    """Loads Leadership test data, placing 'campo_unico' first and then 'item_' fields."""
    leadership_data = Liderazgo.objects.filter(campo_unico=id).values()
    df_leadership = pd.DataFrame(list(leadership_data))

    if not df_leadership.empty:
        item_cols = [col for col in df_leadership.columns if col.startswith('item_')]
        other_cols = [col for col in df_leadership.columns if col not in ['campo_unico'] + item_cols]
        new_order = ['campo_unico'] + item_cols + other_cols
        new_order = [col for col in new_order if col in df_leadership.columns]
        df_leadership = df_leadership[new_order]
    return df_leadership

def get_combined_test_data():
    """Combines personal data with all test data into a single DataFrame."""
    df_personal = load_personal_data()
    df_disc = load_disc_data()
    df_teamwork = load_teamwork_data()
    df_leadership = load_leadership_data()

    all_tests = []

    if not df_disc.empty:
        df_disc['test_type'] = 'DISC'
        all_tests.append(df_disc)

    if not df_teamwork.empty:
        df_teamwork['test_type'] = 'Teamwork'
        all_tests.append(df_teamwork)

    if not df_leadership.empty:
        df_leadership['test_type'] = 'Leadership'
        all_tests.append(df_leadership)

    if not all_tests:
        return pd.DataFrame() # Return empty DataFrame if no test data

    df_all_tests = pd.concat(all_tests, ignore_index=True)

    # Rename 'aplicante_id' to 'id' for merging with personal data
    df_all_tests = df_all_tests.rename(columns={'aplicante_id': 'id'})

    # Merge with personal data
    df_combined = pd.merge(df_personal, df_all_tests, on='id', how='inner')

    return df_combined

if __name__ == '__main__':
    df = load_disc_data('564c90f62b0f416f90f089a0b750fd63')
    print(df)