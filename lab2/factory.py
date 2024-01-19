from player import Player
import xml.etree.ElementTree as ET
import player_pb2 as pb

class PlayerFactory:
    def to_json(self, players: list[Player]):
        json = []
        for player in players:
            json.append({
            "nickname" : player.nickname,
            "email" : player.email,
            "date_of_birth" : player.date_of_birth.strftime("%Y-%m-%d"),
            "xp" : player.xp,
            "class" : player.cls,
        })
        return json

    def from_json(self, list_of_dict: list[dict]):
        _list = []
        for player in list_of_dict:
            _list.append(Player(
                player["nickname"],
                player["email"],
                player["date_of_birth"],
                player["xp"],
                player["class"]
            ))
        return _list

    def from_xml(self, xml_string):
        _list = []
        tree = ET.fromstring(xml_string)
        for stats in tree:
            _list.append(Player(stats[0].text, stats[1].text, stats[2].text, int(stats[3].text), stats[4].text))
        return _list

    def to_xml(self, list_of_players):
        
        _xml = ET.Element('data')
        for players in list_of_players:
            player = ET.Element('player')
            nick = ET.Element('nickname')
            nick.text = players.nickname
            player.append(nick)
            email = ET.Element('email')
            email.text = players.email
            player.append(email)
            dob = ET.Element('date_of_birth')
            dob.text = players.date_of_birth.strftime("%Y-%m-%d")
            player.append(dob)
            xp = ET.Element('xp')
            xp.text = str(players.xp)
            player.append(xp)
            cls = ET.Element('class')
            cls.text = players.cls
            player.append(cls)
            _xml.append(player)
        string = '<?xml version="1.0"?>'
        result = f"{string}{ET.tostring(_xml).decode()}"

        return result

    def from_protobuf(self, binary):
        something = pb.PlayerList()
        pass

    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects intoa binary protobuf string.
        '''
        pass
