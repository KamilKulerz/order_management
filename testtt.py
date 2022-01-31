class Solution:
    # @param A : list of integers
    # @param B : integer
    # @return an integer
    def get_possibilities(self, n, B):
        poss = []
        idxs = list(range(0, n))
        for i in range(B+1):
            beg = idxs[:B-i]
            if i == 0:
                endd = []
            else:
                endd = idxs[-i:]
            row = beg + endd
            poss.append(row)
        return poss

    def solve(self, A, B):
        print(A, B)
        possible = self.get_possibilities(len(A), B)

        maxx = -9999999999999999999999999999999
        for row in possible:
            temp_list = []
            pos_max = 0
            for p in row:
                pos_max += A[p]
            if pos_max > maxx:
                maxx = pos_max
        return maxx


A = [-584, -714, -895, -512, -718, -545, 734, -886, 701, 316, -329, 786, -737, -687, -645, 185, -947, -88, -192, 832, -55, -687, 756, -679, 558, 646, 982, -519, -856, 196, -778, 129, -839, 535, -550, 173, -534, -956, 659, -708, -561, 253, -976, -846, 510, -255, -351, 186, -687, -526, -978, -832, -982, -213, 905, 958,
     391, -798, 625, -523, -586, 314, 824, 334, 874, -628, -841, 833, -930, 487, -703, 518, -823, 773, -730, 763, -332, 192, 985, 102, -520, 213, 627, -198, -901, -473, -375, 543, 924, 23, 972, 61, -819, 3, 432, 505, 593, -275, 31, -508, -858, 222, 286, 64, 900, 187, -640, -587, -26, -730, 170, -765, -167, 711, 760, -104, -333]
B = 32

s = Solution()
print(s.solve(A, B))
