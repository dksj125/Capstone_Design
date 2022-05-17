from neo4j import GraphDatabase

class MakeNode:
    
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth = (user, password))
        
    def close(self):
        self.driver.close()
    
    def create_Contents(self, tx, genre, title, url_link):
        tx.run("CREATE(a:Contents{genre: $genre, Title: $title, url_link : $url_link , likes: 0})",
                               genre = genre,  title = title, url_link = url_link)
        
    
    def Add_Contents(self, title, url_link):
        with self.driver.session() as session:
            return session.write_transaction(self.create_Contents,"Comic", title, url_link)
        
    def Add_Relation(self, genre, title):
        with self.driver.session() as session:
            session.write_transaction(self.RelationWithGenreAndContents, genre, title)
        
    def RelationWithGenreAndContents(self, tx, genre, title):
        tx.run("MATCH(C:Contents), (G:Genre{KindOfGenre: $genre})\
                    WHERE C.genre =  $genre and C.Title = $title\
                    CREATE (G) - [r:Include]->(C)",
                    genre=genre, title=title)