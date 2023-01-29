from pymongo import MongoClient


class Components:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client.ResArcana
        self.artifacts = self.db.artifacts
        self.items = self.db.items
        self.mages = self.db.mages
        self.monuments = self.db.monuments
        self.places_of_power = self.db.placesOfPower
        self.scrolls = self.db.scrolls
        self.sheets = self.db.sheets

    def get_all_components(self, expansions):
        return {
            "artifacts": self.get_artifacts(expansions),
            "items": self.get_items(expansions),
            "mages": self.get_mages(expansions),
            "monuments": self.get_monuments(expansions),
            "places_of_power": self.get_places_of_power(expansions),
            "scrolls": self.get_scrolls(expansions),
            "sheet": self.get_sheet(expansions)
        }

    def get_artifacts(self, expansions):
        return list(self.artifacts.find({'expansion': {"$in": expansions}}, {'_id': 0, 'expansion': 0}))

    def get_items(self, expansions):
        return list(self.items.find({'expansion': {"$in": expansions}}, {'_id': 0, 'expansion': 0}))

    def get_mages(self, expansions):
        return list(self.mages.find({'expansion': {"$in": expansions}}, {'_id': 0, 'expansion': 0}))

    def get_monuments(self, expansions):
        return list(self.monuments.find({'expansion': {"$in": expansions}}, {'_id': 0, 'expansion': 0}))

    def get_places_of_power(self, expansions):
        roll_places = list(self.places_of_power.aggregate([
            {"$group": {
                "_id": "$variation",
                "doc": {"$first": "$$ROOT"}
            }},
            {"$replaceRoot": {
                "newRoot": "$doc"
            }},
            {"$project": {"_id": 0, "type": 0, "variation": 0, "side": 0}}
        ]))
        return [place for place in roll_places if place.get('expansion') in expansions]

    def get_scrolls(self, expansions):
        return list(self.scrolls.find({'expansion': {"$in": expansions}}, {'_id': 0, 'expansion': 0}))

    def get_sheet(self, expansions):
        return self.sheets.find_one({'expansion': expansions[0]}, {'_id': 0, 'expansion': 0})


if __name__ == '__main__':
    a = Components().get_all_components(("Base", "LAT", "PI"))
    print(a)
