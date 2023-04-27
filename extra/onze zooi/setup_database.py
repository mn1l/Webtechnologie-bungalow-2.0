from Database import db, Klant

db.create_all() # Creeer

...             # Klanten toevoegen hier bijv. Sander = Klant('Sander', 'Sander@gmail.com', 'Sander')

db.session.add_all() # Voeg iedereen toe

db.session.commit() # Commit alles

klanten = Klant.query.all() # Roep alle klanten op in de database

#Crud gebruiken om dingen te verwijderen -> Week6
