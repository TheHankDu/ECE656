import math
import collections

def entropy(rows: list) -> float:
    """
    Calculate entropy for a list
    :param rows:
    :return:
    """
    result = collections.Counter()
    result.update(rows)
    rows_len = len(rows)
    assert rows_len   #rows_len cannot be 0
    ent = 0.0
    for r in result.values():
        p = float(r) / rows_len
        ent -= p * math.log2(p)
    return ent

def condition_entropy(feature_list: list, result_list: list) -> float:
    """
    Calculate Condition Entropy
    """
    entropy_dict = collections.defaultdict(list)  # {0:[], 1:[]}
    for feature, value in zip(feature_list, result_list):
        entropy_dict[feature].append(value)
    ent = 0.0
    feature_len = len(feature_list)
    for value in entropy_dict.values():
        p = len(value) / feature_len * entropy(value)
        ent += p

    return ent

def gain(feature_list: list, result_list: list) -> float:
    info = entropy(result_list)
    info_condition = condition_entropy(feature_list, result_list)
    return info - info_condition


class DecisionNode(object):
    def __init__(self, condition=-1, data_set=None, labels=None, results=None, tb=None, fb=None):
        self.has_calc_index = []    # Calculated
        self.condition = condition        
        self.data_set = data_set  
        self.labels = labels        # matched value
        self.results = results      
        self.tb = tb                # subtree whose gain is True
        self.fb = fb                # subtree whose gain is False

def if_split_end(result_list: list) -> bool:
    """
    Condition for Ending Recursion
    :param result_list:
    :return:
    """
    result = collections.Counter()
    result.update(result_list)
    return len(result) == 1

def choose_best_feature(data_set: list, labels: list, ignore_index: list) -> int:
    """
    Choose the best feature and return index
    """
    result_dict = {}  # { Index: Gain }
    feature_num = len(data_set[0])
    for i in range(feature_num):
        if i in ignore_index:
            continue
        feature_list = [x[i] for x in data_set]
        result_dict[i] = gain(feature_list, labels) 
    ret = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    return ret[0][0]


class DecisionTreeClass():
    def __init__(self):
        self.feature_num = 0      
        self.tree_root = None

    def build_tree(self, node: DecisionNode):
        if if_split_end(node.labels):
            node.results = node.labels[0]
            return
        #print(node.data_set)
        # create new path
        best_index = choose_best_feature(node.data_set, node.labels, node.has_calc_index)
        node.condition = best_index

        # left subtree
        tb_index = [i for i, value in enumerate(node.data_set) if value[best_index]]
        tb_data_set     = [node.data_set[x] for x in tb_index]
        tb_data_labels  = [node.labels[x] for x in tb_index]
        tb_node = DecisionNode(data_set=tb_data_set, labels=tb_data_labels)
        tb_node.has_calc_index = list(node.has_calc_index)
        tb_node.has_calc_index.append(best_index)
        node.tb = tb_node

        # right subtree
        fb_index = [i for i, value in enumerate(node.data_set) if not value[best_index]]
        fb_data_set = [node.data_set[x] for x in fb_index]
        fb_data_labels = [node.labels[x] for x in fb_index]
        fb_node = DecisionNode(data_set=fb_data_set, labels=fb_data_labels)
        fb_node.has_calc_index = list(node.has_calc_index)
        fb_node.has_calc_index.append(best_index)
        node.fb = fb_node

        # Recursion
        if tb_index:
            self.build_tree(node.tb)
        if fb_index:
            self.build_tree(node.fb)

    def clean_tree_example_data(self, node: DecisionNode):
        """
        Clean Tree
        :return:
        """
        del node.has_calc_index
        del node.labels
        del node.data_set
        if node.tb:
            self.clean_tree_example_data(node.tb)
        if node.fb:
            self.clean_tree_example_data(node.fb)

    def fit(self, train_set: list, result_set: list):
        """
        train_set is 2D
        result_set is 1D
        """
        self.feature_num = len(train_set[0])
        self.tree_root = DecisionNode(data_set=train_set, labels=result_set)
        self.build_tree(self.tree_root)
        self.clean_tree_example_data(self.tree_root)

    def _predict(self, data_test: list, node: DecisionNode):
        if node.results:
            return node.results
        condition = node.condition
        if data_test[condition]:
            return self._predict(data_test, node.tb)
        else:
            return self._predict(data_test, node.fb)

    def predict(self, data_test):
        return self._predict(data_test, self.tree_root)


if __name__ == "__main__":
    dummy_x = (
        (0, 20, 110, 50, 121, 4321, 430, 60, 51, 0, ),
        (0, 0, 5241, 156, 0, 141, 0, 0, 13, 0, ),
        (1, 0, 134, 0, 1, 1, 0, 0, 1, 0, ),
        (0, 1, 0, 0, 1, 0, 0, 1, 1, 0, ),
        (0, 1, 0, 0, 1, 0, 1, 0, 0, 1, ),
        (0, 1, 0, 1, 0, 0, 1, 0, 0, 1, ),
        (1, 0, 0, 1, 0, 0, 1, 0, 0, 1, ),
        (0, 0, 1, 0, 1, 0, 0, 1, 1, 0, ),
        (0, 0, 1, 0, 1, 0, 1, 0, 0, 1, ),
        (0, 1, 0, 0, 1, 0, 0, 1, 0, 1, ),
        (0, 0, 1, 1, 0, 0, 0, 1, 0, 1, ),
        (1, 0, 0, 1, 0, 0, 0, 1, 1, 0, ),
        (1, 0, 0, 0, 1, 1, 0, 0, 0, 1, ),
        (0, 1, 0, 1, 0, 0, 0, 1, 1, 0, ),
    )
    dummy_y = [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0]

    tree = DecisionTreeClass()
    tree.fit(dummy_x, dummy_y)

    test_row = [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, ]
    print(tree.predict(test_row))