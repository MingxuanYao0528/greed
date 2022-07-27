import z3

from SEtaac.utils.solver.base import Solver


def simplify_result(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return z3.simplify(res)
    return wrapper


class Z3(Solver):
    """
    This is a singleton class, and all methods are static
    """

    def __init__(self, partial_init=False):
        self.assertions = list()
        if partial_init is True:
            return
        self._config_z3()
        self.solver = z3.SolverFor('QF_ABV')
    
    def _config_z3(self):
        # SEE HERE THE LIST OF POSSIBLE CONFIGURATIONS
        # https://pythonmana.com/2022/04/202204161602015923.html

        z3.set_param('rewriter.blast_select_store', True)
        z3.set_param('rewriter.sort_store', True)
        z3.set_param('rewriter.expand_nested_stores', True)
        z3.set_param('rewriter.expand_select_ite', True)
        z3.set_param('rewriter.expand_store_eq', True)
        z3.set_param('rewriter.pull_cheap_ite', True)
        z3.set_param('rewriter.bv_ite2id', True)
        
        #z3.set_param('rewriter.rewrite_patterns', True)
        #z3.set_param('rewriter.cache_all', True)
        
        return

    def BVSort(self, width):
        return z3.BitVecSort(width)

    def BVV(self, value, width):
        return z3.BitVecVal(value, width)

    def BVS(self, symbol, width):
        return z3.BitVec(symbol, width)

    def bv_unsigned_value(self, bv):
        return int(bv.as_binary_string(), 2)

    def is_concrete(self, bv):
        return z3.is_bv_value(bv)

    def is_sat(self, ):
        return self.solver.check() == z3.sat

    def is_unsat(self, ):
        return self.solver.check() == z3.unsat

    def is_formula_sat(self, formula):
        self.push()
        self.add_assertion(formula)
        sat = self.is_sat()
        self.pop()

        return sat
    
    def bv_size(self, bv):
        return bv.size()

    def push(self, ):
        # Create a Z3 backtracking point
        self.solver.push()

    def pop(self, ):
        # Remove a Z3 backtracking point
        self.solver.pop()

    def add_assertion(self, formula):
        self.solver.add(formula)
        self.assertions.append(formula)

    def add_assertions(self, formulas):
        self.solver.add(*formulas)
        self.assertions += formulas

    def add_assumption(self, formula):
        raise Exception

    def add_assumptions(self, formulas):
        raise Exception

    def reset_assumptions(self, ):
        raise Exception

    def fixate_assumptions(self, ):
        raise Exception

    def simplify_formula(self, formula):
        return z3.simplify(formula)

    def Array(self, symbol, index_sort, value_sort):
        return z3.Array(symbol, index_sort, value_sort)

    def ConstArray(self, symbol, index_sort, value_sort, default):
        raise Exception

    # CONDITIONAL OPERATIONS

    @simplify_result
    def If(self, cond, value_if_true, value_if_false):
        return z3.If(cond, value_if_true, value_if_false)

    # BOOLEAN OPERATIONS

    @simplify_result
    def Or(self, *terms):
        return z3.Or(*terms)

    @simplify_result
    def And(self, *terms):
        return z3.And(*terms)

    @simplify_result
    def Not(self, term):
        return z3.Not(term)

    # BV OPERATIONS

    @simplify_result
    def Equal(self, a, b):
        return z3.BitVecRef.__eq__(a,b)
    
    @simplify_result
    def NotEqual(self, a, b):
        return z3.BitVecRef.__ne__(a,b)

    @simplify_result
    def BV_Extract(self, start, end, bv):
        # Z3 extract is (start_offset, length, symbol)
        return z3.Extract(end, start, bv)

    @simplify_result
    def BV_Concat(self, terms):
        res = z3.Concat(terms[0], terms[1])
        for i in range(2, len(terms)):
            res = z3.Concat(res, terms[i])
        return res

    @simplify_result
    def BV_Add(self, a, b):
        return z3.BitVecRef.__add__(a,b)

    @simplify_result
    def BV_Sub(self, a, b):
        return z3.BitVecRef.__sub__(a,b)

    @simplify_result
    def BV_Mul(self, a, b):
        return z3.BitVecRef.__mul__(a,b)

    @simplify_result
    def BV_UDiv(self, a, b):
        return z3.UDiv(a, b)

    @simplify_result
    def BV_SDiv(self, a, b):
        return z3.BitVecRef.__div__(a,b)

    @simplify_result
    def BV_SMod(self, a, b):
        return z3.BitVecRef.__mod__(a,b)

    @simplify_result
    def BV_SRem(self, a, b):
        return z3.SRem(a,b)

    @simplify_result
    def BV_URem(self, a, b):
        return z3.URem(a, b)

    @simplify_result
    def BV_Sign_Extend(self, a, b):
        return z3.SignExt(b,a)

    @simplify_result
    def BV_Zero_Extend(self, a, b):
        return z3.ZeroExt(b,a)

    @simplify_result
    def BV_UGE(self, a, b):
        return z3.UGE(a, b)

    @simplify_result
    def BV_ULE(self, a, b):
        return z3.ULE(a, b)

    @simplify_result
    def BV_UGT(self, a, b):
        return z3.UGT(a, b)

    @simplify_result
    def BV_ULT(self, a, b):
        return z3.ULT(a, b)

    @simplify_result
    def BV_SGE(self, a, b):
        return z3.BitVecRef.__ge__(a,b)

    @simplify_result
    def BV_SLE(self, a, b):
        return z3.BitVecRef.__le__(a,b)

    @simplify_result
    def BV_SGT(self, a, b):
        return z3.BitVecRef.__gt__(a,b)

    @simplify_result
    def BV_SLT(self, a, b):
        return z3.BitVecRef.__lt__(a,b)

    @simplify_result
    def BV_And(self, a, b):
        return z3.BitVecRef.__and__(a,b)

    @simplify_result
    def BV_Or(self, a, b):
        return z3.BitVecRef.__or__(a,b)

    @simplify_result
    def BV_Xor(self, a, b):
        return z3.BitVecRef.__xor__(a,b)

    @simplify_result
    def BV_Not(self, a):
        return z3.BitVecRef.__invert__(a)

    @simplify_result
    def BV_Shl(self, a, b):
        return z3.BitVecRef.__lshift__(a,b)

    @simplify_result
    def BV_Shr(self, a, b):
        return z3.BitVecRef.__rshift__(a,b)

    @simplify_result
    def BV_Sar(self, a, b):
        # (n&msb) | (n>>shift)
        '''
        msb_set = self.BV_Extract(255, 255, a)
        shift_mask = self.BV_Shr(self.BVV(2 ** 256 - 1, 256), b)

        shifted = self.BV_Shr(a, b)
        res = self.If(msb_set,
                      self.BV_Or(shifted, self.BV_Not(shift_mask)),
                      self.BV_And(shifted, shift_mask))
        '''
        res_shift1 = self.BV_Shr(a, b)
        res_shift2 = self.BV_Extract(0, 255-self.bv_unsigned_value(b),res_shift1)
        res = self.BV_Sign_Extend(res_shift2, 256-self.bv_size(res_shift2))
        return res

    # ARRAY OPERATIONS

    @simplify_result
    def Array_Store(self, arr, index, elem):
        return z3.Store(arr, index, elem)

    @simplify_result
    def Array_Select(self, arr, index):
        return z3.Select(arr, index)

    # def eval_one_array(self, array, length):
    #     self.is_sat()
    #     return [int(self.Array_Select(array, self.BVV(i, 256)).assignment, 2) for i in
    #             range(length)]

    def copy(self):
        new_solver = Z3(partial_init=True)
        new_solver.solver = self.solver.translate(self.solver.ctx)
        new_solver.add_assertions(self.assertions)

        return new_solver
