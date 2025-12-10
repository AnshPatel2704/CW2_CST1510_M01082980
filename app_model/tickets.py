import pandas as pd
def  migrating_it_tickets(conn):
    data = pd.read_csv('DATA/it_tickets.csv')
    data.t0_sql('it_tickets', conn)
    