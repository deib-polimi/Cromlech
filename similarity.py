import ast
import numbers
import sys

def check_if_same_service(o1, o2, arch):
    for m in arch:
        if o1 in m and o2 in m:
            return True
    return False


def compute_similarity(sol1, sol2):
    f1 = open(sol1, "r")
    f2 = open(sol2, "r")
    
    f1_content = f1.read()
    f2_content = f2.read()

    a = ast.literal_eval(f1_content)
    b = ast.literal_eval(f2_content)

    attributes_set = set()
    ops_set = set()
    for m in a:
        for elem in m:
            if isinstance(elem, numbers.Number):
                ops_set.add(elem)
            else:
                attributes_set.add(elem.replace('R', '').replace('P', '').replace('N', ''))
    attr_num = len(attributes_set)
    op_num = len(ops_set)
    
    print("Op: " + str(op_num) + ". Attr: " + str(attr_num))
    
    to_remove = []
    for n in a:
        rem = []
        for y in n:
            if isinstance(y, str):
                rem.append(y)
        to_remove.append(rem)
    i = 0
    for n in a:
        for t in to_remove[i]:
            n.remove(t)

        i += 1
        
    total_couples = (op_num-1)**2 + op_num - 1
    dict_a = {}
    dict_b = {}
    for i in range(0, op_num-1):
        for j in range(i+1, op_num):
            dict_a.update({(i, j): check_if_same_service(i, j, a)})
            dict_b.update({(i, j): check_if_same_service(i, j, b)})

    true_a = len([x for x in dict_a.values() if x])
    false_a = len([x for x in dict_a.values() if not x])
    true_b = len([x for x in dict_b.values() if x])
    false_b = len([x for x in dict_b.values() if not x])
    both_present = 0
    present_in_a_only = 0
    present_in_b_only = 0
    both_absent = 0
    for i in range(0, op_num - 1):
        for j in range(i + 1, op_num):
            if dict_a.get((i, j)):
                if dict_b.get((i, j)):
                    both_present += 1
                else:
                    present_in_a_only += 1
            else:
                if dict_b.get((i, j)):
                    present_in_b_only += 1
                else:
                    both_absent += 1
    operation_similarity = (both_present + both_absent - present_in_a_only - present_in_b_only)*2/total_couples

    to_remove = []
    for n in a:
        rem = []
        for y in n:
            if isinstance(y, int) or not y.endswith('P'):
                rem.append(y)
        to_remove.append(rem)
    i = 0
    for n in a:
        for t in to_remove[i]:
            n.remove(t)
        i += 1
    to_remove = []
    for n in b:
        rem = []
        for y in n:
            if isinstance(y, int) or not y.endswith('P'):
                rem.append(y)
        to_remove.append(rem)
    i = 0
    for n in b:
        for t in to_remove[i]:
            n.remove(t)
        i += 1
    total_couples = (attr_num-1)**2 + attr_num - 1
    dict_a = {}
    dict_b = {}
    for i in range(0, attr_num-1):
        for j in range(i+1, attr_num):
            a1 = str(100000 + i) + 'P'
            a2 = str(100000 + j) + 'P'
            dict_a.update({(a1, a2): check_if_same_service(a1, a2, a)})
            dict_b.update({(a1, a2): check_if_same_service(a1, a2, b)})
    true_a = len([x for x in dict_a.values() if x])
    false_a = len([x for x in dict_a.values() if not x])
    true_b = len([x for x in dict_b.values() if x])
    false_b = len([x for x in dict_b.values() if not x])
    both_present = 0
    present_in_a_only = 0
    present_in_b_only = 0
    both_absent = 0
    for i in range(0, attr_num - 1):
        for j in range(i + 1, attr_num):
            if dict_a.get((str(100000 + i) + 'P', str(100000 + j) + 'P')):
                if dict_b.get((str(100000 + i) + 'P', str(100000 + j) + 'P')):
                    both_present += 1
                else:
                    present_in_a_only += 1
            else:
                if dict_b.get((str(100000 + i) + 'P', str(100000 + j) + 'P')):
                    present_in_b_only += 1
                else:
                    both_absent += 1
    data_similarity = (both_present + both_absent - present_in_a_only - present_in_b_only)*2/total_couples
    return operation_similarity, data_similarity

if __name__ == '__main__':
    operation_similarity, data_similarity = compute_similarity(sys.argv[1], sys.argv[2])
    print("OP SIMILARITY:", operation_similarity,"DATA SIMILARITY:", data_similarity)
