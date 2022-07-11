import preprocessing as m

def check_if_same_service(o1, o2, arch):
    for m in arch:
        if o1 in m and o2 in m:
            return True
    return False

if __name__ == '__main__':
    op_num = 124
    attr_num = 137
    # Copy here the solver output of first architecture
    a = [[11, 13, 14, 15, 18, 19, 22, 23, 24, 25, 26, 31, 39, 40, 43, 44, 52, 56, 59, 60, 62, 66, 67, 68, '100022P', '100023R', '100024P', '100031P', '100032P', '100033P', '100034P', '100035P', '100036P', '100037P', '100038P', '100039P', '100040P', '100041N', '100042P', '100043R', '100044P', '100045N', '100046P', '100047P', '100048P', '100049P', '100050P', '100051P', '100052N', '100053N', '100054N', '100055R', '100056R', '100057N', '100058P', '100059P', '100081P', '100082P', '100083P', '100084P', '100085P', '100086P', '100096P', '100097P', '100098P', '100099P', '100100P', '100101P', '100121N', '100123R', '100124P', '100125P', '100127N', '100128N', '100129P', '100130N', '100133N', '100135P', '100136P', '100137P', '100138P', '100139P', '100140P', '100144P', '100145P', '100146P', '100147P', '100148P', '100149P', '100150P', '100151P', '100152P', '100153P', '100154P', '100155P', '100156P', '100157P', '100158P', '100159P', '100160P', '100161P', '100162P', '100163P', '100164P', '100165P'], [10, 17, 20, 28, 45, 53, 54, 65, '100000P', '100001P', '100002P', '100003P', '100004P', '100005P', '100006P', '100007P', '100008P', '100009P', '100010P', '100011P', '100012P', '100013P', '100014P', '100015P', '100016P', '100017P', '100018P', '100019P', '100020P', '100021P', '100032R', '100033R', '100034R', '100035R', '100036R', '100037R', '100038R', '100045N', '100054N', '100055R', '100056R', '100072P', '100074P'], [6, 7, 8, 12, 16, 27, 33, 34, 35, 36, 37, 38, 41, 42, 46, 47, 48, 50, 57, 58, '100011R', '100020R', '100023P', '100025P', '100026P', '100027P', '100028N', '100029R', '100030N', '100059R', '100060P', '100061P', '100062P', '100063P', '100064P', '100065P', '100066P', '100067P', '100068P', '100069N', '100070N', '100071N', '100073P', '100074N', '100075P', '100076P', '100077P', '100078P', '100079P', '100080P', '100087P', '100088P', '100089P', '100090P', '100091P', '100092P', '100093P', '100094N', '100095P', '100102P', '100103P', '100104P', '100105P', '100106P', '100107P', '100108P', '100109P', '100110P', '100111P', '100112P', '100113P', '100114P', '100115P', '100116P', '100117P', '100118P', '100119P', '100120P', '100122P', '100128N', '100129R', '100130R', '100131N', '100132N', '100134N', '100141P', '100142P', '100143P', '100144R', '100155R'], [0, 1, 2, 3, 4, 5, 9, 21, 29, 30, 32, 49, 51, 55, 61, 63, 64, '100022R', '100023N', '100024N', '100028P', '100029P', '100030P', '100041P', '100043P', '100045P', '100052P', '100053P', '100054P', '100055P', '100056P', '100057P', '100069P', '100070P', '100071P', '100094P', '100121P', '100123P', '100124R', '100125R', '100126P', '100127P', '100128P', '100129R', '100130P', '100131P', '100132P', '100133P', '100134P', '100141R', '100142R', '100143R', '100144R']]
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
    # Copy here the solver output of second architecture
    b = [[7, 27, 33, 34, 35, 36, 38, 41, 46, 47, 48, 51, '100011N', '100020N', '100023N', '100025P', '100026P', '100027P', '100028P', '100029P', '100030P', '100059P', '100069P', '100073P', '100074R', '100075P', '100076P', '100077P', '100078P', '100079P', '100080P', '100087P', '100088P', '100089P', '100090P', '100091P', '100092P', '100093P', '100094R', '100102P', '100103P', '100104P', '100105P', '100106P', '100107P', '100108P', '100109P', '100110P', '100111P', '100112P', '100113P', '100114P', '100115P', '100116P', '100117P', '100118P', '100119P', '100120P', '100122P', '100128R', '100129R', '100130N', '100141P', '100142P', '100143P', '100144P', '100155N'], [10, 17, 20, 28, 45, 53, 54, 65, '100000P', '100001P', '100002P', '100003P', '100004P', '100005P', '100006P', '100007P', '100008P', '100009P', '100010P', '100011P', '100012P', '100013P', '100014P', '100015P', '100016P', '100017P', '100018P', '100019P', '100020P', '100021P', '100032R', '100033R', '100034R', '100035R', '100036R', '100037R', '100038R', '100045N', '100054N', '100055N', '100056N', '100072P', '100074P'], [6, 8, 12, 13, 14, 16, 18, 19, 37, 39, 40, 42, 43, 44, 50, 57, 58, 59, 62, '100025R', '100026R', '100029R', '100060P', '100061P', '100062P', '100063P', '100064P', '100065P', '100066P', '100067P', '100068P', '100070R', '100071P', '100081P', '100082P', '100083P', '100084P', '100085P', '100086P', '100095P', '100096P', '100097P', '100098P', '100099P', '100100P', '100101P', '100131N', '100132P', '100134N', '100135P', '100136N', '100137N', '100138P', '100139N', '100140N'], [0, 1, 2, 3, 4, 5, 9, 11, 15, 21, 22, 23, 24, 25, 26, 29, 30, 31, 32, 49, 52, 55, 56, 60, 61, 63, 64, 66, 67, 68, '100022P', '100023P', '100024P', '100031P', '100032P', '100033P', '100034P', '100035P', '100036P', '100037P', '100038P', '100039P', '100040P', '100041P', '100042P', '100043P', '100044P', '100045P', '100046P', '100047P', '100048P', '100049P', '100050P', '100051P', '100052P', '100053P', '100054P', '100055P', '100056P', '100057P', '100058P', '100059R', '100069R', '100070P', '100071R', '100081R', '100082R', '100083R', '100084R', '100085R', '100086R', '100094P', '100096R', '100097R', '100098R', '100099R', '100100R', '100101R', '100121P', '100123P', '100124P', '100125P', '100126P', '100127P', '100128P', '100129P', '100130P', '100131P', '100132R', '100133P', '100134P', '100135R', '100136P', '100137P', '100138R', '100139P', '100140P', '100144R', '100145P', '100146P', '100147P', '100148P', '100149P', '100150P', '100151P', '100152P', '100153P', '100154P', '100155P', '100156P', '100157P', '100158P', '100159P', '100160P', '100161P', '100162P', '100163P', '100164P', '100165P']]
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
    score = (both_present + both_absent - present_in_a_only - present_in_b_only)*2/total_couples
    print("OPERATION SIMILARITY:" + str(score))

    attr_num = 137
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
    score = (both_present + both_absent - present_in_a_only - present_in_b_only)*2/total_couples
    print("DATA SIMILARITY:" + str(score))