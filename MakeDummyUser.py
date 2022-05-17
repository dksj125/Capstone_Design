from neo4j import GraphDatabase
import random

class MakeUserNode:
    
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth = (user, password))
        
    def close(self):
        self.driver.close()
    
    def create_User(self, tx, name, best_genre, recent_search):
        tx.run("CREATE(a:User{name: $name, best_genre: $best_genre, recent_search:$recent_search})",
                               name = name,  best_genre = best_genre, recent_search = recent_search)
        
    
    def Add_User(self, Name, best_genre, recent_search):
        with self.driver.session() as session:
            return session.write_transaction(self.create_User,Name, best_genre, recent_search)
        
    def Add_Relation(self, Name, genre):
        with self.driver.session() as session:
            session.write_transaction(self.RelationWithGenreAndUser, Name, genre)
        
    def RelationWithGenreAndUser(self, tx, name, genre):
        tx.run("MATCH(U:User), (G:Genre{KindOfGenre: $genre})\
                    WHERE U.best_genre =  $genre and U.name = $name\
                    CREATE (U) - [r:BestGenre]->(G)",
                    genre=genre, name = name)
        

    def RelationWithGenreAndContents(self, tx, genre, title):
        tx.run("MATCH(C:Contents), (G:Genre{KindOfGenre: $genre})\
                    WHERE C.genre =  $genre and C.Title = $title\
                    CREATE (G) - [r:Include]->(C)",
                    genre=genre, title=title)        

FamilyName = ['정', '한', '김', '전', '여', '변', '문', '나', '박', '주', '이', '강']

FirstName = ['지수', '부교', '민기', '채원', '동규', '범수', '도한', '관수', '유빈', '해인', '다정']

Name = []

Genre = ['Comic', 'Action', 'Sing', 'Sad']

UserList = []

for i in FamilyName:
    for j in FirstName:
        Name.append(i+j)
        
for i in Name:
    UserList.append([i, random.choice(Genre)])
    
node = MakeUserNode("bolt://localhost:7687", "neo4j", "wltn1018")

for i in UserList:
    node.Add_User(i[0], i[1], "empty")
    
for i in UserList:
    node.Add_Relation(i[0], i[1])
    
    
node.close()
    

