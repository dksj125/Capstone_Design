from neo4j import GraphDatabase
import random

class MakeNodeWatchMovie:
    
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth = (user, password))
        
    def close(self):
        self.driver.close()
        
    def Add_Relation(self, name, title):
        with self.driver.session() as session:
            session.write_transaction(self.RelationWithUserAndContents, name, title)
            
    def Incre_Like(self, name, title):
        with self.driver.session() as session:
            session.write_transaction(self.UserLikeContents, name, title)
            
    def UserLikeContents(self, tx, name, title):
        tx.run("MATCH(C:Contents), (U:User{name: $name})\
                    WHERE C.Title =  $title and U.name = $name\
                    SET C.likes = C.likes + 1\
                    CREATE (U) - [r:Like]->(C)",
                    name=name, title=title)
        
        
    def RelationWithUserAndContents(self, tx, name, title):
        tx.run("MATCH(C:Contents), (U:User{name: $name})\
                    WHERE C.Title =  $title and U.name = $name\
                    CREATE (U) - [r:Watch]->(C)",
                    name=name, title=title)
        
    def ReadMovieData(self):
        with self.driver.session() as session:
            MovieData =  session.run("MATCH(n:Contents) RETURN n.Title, n.genre")
            
            Movielist = []
            
            for i in MovieData:
                
                dummy = []
                
                dummy.append(i["n.Title"])
                
                dummy.append(i["n.genre"])
                
                Movielist.append(dummy)
    
            return Movielist
        
    def ReadUserData(self):
        with self.driver.session() as session:
            
            UserData =  session.run("MATCH(n:User) RETURN n.name, n.best_genre")
            
            UserList = []
            
            for i in UserData:
                
                dummy = []
                
                dummy.append(i["n.name"])
                
                dummy.append(i["n.best_genre"])
                
                UserList.append(dummy)
    
                
            return UserList


node = MakeNodeWatchMovie("bolt://localhost:7687", "neo4j", "wltn1018")

MovieDataList = node.ReadMovieData()
UserDataList = node.ReadUserData()

ComicMovieDataList = []

ActionMovieDataList = []

SingMovieDataList = []

SadMovieDataList = []

for i in MovieDataList:
    
    if(i[1] =="Comic"):
        ComicMovieDataList.append(i)
    
    elif(i[1] == "Action"):
        ActionMovieDataList.append(i)
    
    elif(i[1] == "Sing"):
        SingMovieDataList.append(i)
    
    elif(i[1] == "Sad"):
        SadMovieDataList.append(i)


for i in UserDataList:
    count  = 0
    like = [True, False]
    index = 1
    if(i[1] == "Comic"):
        SampleList = random.sample(ComicMovieDataList, 10)
        
    elif(i[1] == "Action"):
        SampleList = random.sample(ActionMovieDataList, 10)
        
    elif(i[1] == "Sing"):
        SampleList = random.sample(SingMovieDataList, 10)
        
    else:
        SampleList = random.sample(SadMovieDataList, 10)
    
    for j in SampleList:
        
        node.Add_Relation(i[0], j[0])
        
        if(random.choice(like)):
            node.Incre_Like(i[0], j[0])

node.close()