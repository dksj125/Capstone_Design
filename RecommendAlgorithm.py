from neo4j import GraphDatabase

class RecommendMovie:
    
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth = (user, password))
        
    def close(self):
        self.driver.close()
        

    def RecommendContentsForUsersBestGenre(self, name):
        with self.driver.session() as session:
            
            BestGenreMovies =  session.run("MATCH(u:User), (C:Contents) \
                                                    Where u.name = $name and C.genre = u.best_genre\
                                                    RETURN  C.Title,C.likes ,C.url_link",
                                                    name = name)
            
            RecommendList = {}
            
            for i in BestGenreMovies:

                RecommendList[i["C.url_link"]] = i["C.likes"]
            
            return RecommendList
    
    def RecommendContentsForSearch(self, name):
        
        with self.driver.session() as session:
            
            BestGenreMovies =  session.run("MATCH(u:User), (C:Contents) \
                                                    Where u.name = $name and C.genre = u.recent_search\
                                                    RETURN  C.Title,C.likes ,C.url_link",
                                                    name = name)
            
            RecommendList = {}
            
            for i in BestGenreMovies:

                RecommendList[i["C.url_link"]] = i["C.likes"]
            
            return RecommendList

User = "한지수"

node = RecommendMovie("bolt://localhost:7687", "neo4j", "wltn1018")

BestGenreRecommend = node.RecommendContentsForUsersBestGenre(User)

SearchGenreRecommend = node.RecommendContentsForSearch(User)

BestGenreRecommendList = []

SearchGenreRecommendList = []

for i in range(3):
    dummy = max(BestGenreRecommend, key=BestGenreRecommend.get)
    BestGenreRecommendList.append(dummy)
    BestGenreRecommend.pop(dummy)

for i in range(3):
    dummy = max(SearchGenreRecommend, key=SearchGenreRecommend.get)
    SearchGenreRecommendList.append(dummy)
    SearchGenreRecommend.pop(dummy)

