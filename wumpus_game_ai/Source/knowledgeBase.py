from pysat.solvers import Glucose3
import copy

class KnowledgeBase:
    def __init__(self):
        self.KB = []


    @staticmethod
    def standardize_clause(clause):
        return sorted(list(set(clause)))


    def add_clause(self, clause):
        clause = self.standardize_clause(clause)
        if clause not in self.KB:
            self.KB.append(clause)


    def del_clause(self, clause):
        clause = self.standardize_clause(clause)
        if clause in self.KB:
            self.KB.remove(clause)


    def infer(self, not_alpha):
        # Create a deep copy of the knowledge base
        extended_kb = copy.deepcopy(self.KB)
        
        # Add the negated clause not_alpha to the extended knowledge base
        extended_kb.append([not_alpha])
        
        # Check each clause in the extended knowledge base
        for clause in extended_kb:
            # Check if the clause is valid
            is_valid = self.is_clause_valid(clause, extended_kb)
            
            # If any clause is invalid, return False
            if not is_valid:
                return False
        
        # If all clauses are valid, return True
        return True
    
    def is_clause_valid(self, clause, extended_kb):
        # Check if a clause can be satisfied
        for literal in clause[0]:  # Extract the literals from the inner list
            # If a positive literal is not negated and not in the extended knowledge base, return True
            if literal > 0 and [-literal] not in extended_kb:
                return True
            # If a negative literal is not in the extended knowledge base, return True
            elif literal < 0 and [-literal] not in extended_kb:
                return True
        
        # If no valid cases found, return False
        return False