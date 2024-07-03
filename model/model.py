import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestSet = []
        self._bestScore = 0

    def getBestSet(self, a1, dTot):
        self._bestSet = []
        self._bestScore = 0
        parziale = [a1]
        connessa = nx.node_connected_component(self._graph, a1)
        connessa.remove(a1)
        self._ricorsione(parziale, dTot, connessa)

        return set(self._bestSet), self._bestScore

    def _ricorsione(self, parziale, dTot, connessa):
        if self.durataTot(parziale) > dTot:
            return

        if len(parziale) > len(self._bestSet):
            self._bestSet = copy.deepcopy(parziale)
            self._bestScore = len(parziale)

        for e in connessa:
            if e not in parziale:
                parziale.append(e)
                self._ricorsione(parziale, dTot, connessa)
                parziale.pop()

    def durataTot(self, listOfNodes):
        dtot = 0
        for n in listOfNodes:
            dtot += n.totD
        return toMinutes(dtot)

    def buildGraph(self, d):
        self._graph.clear()
        self._graph.add_nodes_from(DAO.getAlbums(toMillisec(d)))
        self._idMap = {a.AlbumId: a for a in list(self._graph.nodes)}
        edges = DAO.getEdges(self._idMap)
        self._graph.add_edges_from(edges)

    def getConnessaDetails(self, v0):
        conn = nx.node_connected_component(self._graph, v0)
        durataTOT = 0
        for album in conn:
            durataTOT += toMinutes(album.totD)

        return len(conn), durataTOT
    def getGraphDeails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getNodes(self):
        return list(self._graph.nodes)

    def getGraphSize(self):
        return len(self._graph.nodes), len(self._graph.edges)

def toMillisec(d):
    return d*60*1000

def toMinutes(d):
    return d/1000/60