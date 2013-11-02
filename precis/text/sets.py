class Sets:

    @classmethod
    def union(cls,set_a,set_b):
        return list(set(set_a + set_b))

    @classmethod
    def union_all(cls,lists):
        union_list = []
        for list_set in lists:
            union_list = cls.union(union_list,list_set)
        return union_list