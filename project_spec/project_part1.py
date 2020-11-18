def WAND_Algo(query_terms, top_k, inverted_index):
    U, candidates = {}, []
    for t in query_terms:
        U[t] = max([i[1] for i in inverted_index[t]])
        c_t = inverted_index[t][0][0]
        w_t = inverted_index[t][0][1]
        print(t, inverted_index[t])
        candidates.append([t, c_t, w_t])

    threshold = float('-inf')
    Ans = []
    full_eva_count = 0

    while candidates:
        candidates.sort(key=lambda x : x[1])
        print('candidates:',candidates)
        print('query_terms:',query_terms)
        print('U:', U)
        score_limit = 0
        pivot = None
        for t in candidates:
            tmp_s_limit = score_limit + U[t[0]]
            if tmp_s_limit > threshold:
                pivot = t[0]
                break
            score_limit = tmp_s_limit

        if pivot is None:
            break

        c_0 = candidates[0][1]
        c_pivot = DocInfo(candidates, pivot)[0]
        print('c_0', c_0,'c_pivot', c_pivot,'pivot', pivot,'threshold', threshold)
        if c_0 == c_pivot:
            print("plus one "* 10)
            full_eva_count += 1
            s = 0
            I_update = []
            for t in range(len(candidates)):
                if t >= len(candidates): break
                c_t, w_t = DocInfo(candidates, candidates[t][0])
                if c_t != c_pivot: break
                s += w_t
                I_update.append(candidates[t][0])

            for t in I_update:
                candidates = next_posting(candidates, inverted_index, t)
                candidates.sort(key=lambda x : x[1])

            print('new' * 5, candidates)
            if s > threshold:
                Ans.append((s, c_pivot))
                if len(Ans) > top_k:
                    smallest = min([i for i in Ans], key=lambda x : x[0])
                    smallest = max([i for i in Ans if i[0]== smallest[0]], key=lambda x : x[1])
                    Ans.remove(smallest)
                    threshold = min([i[0] for i in Ans])
        else:
            if len(candidates) == 1:
                candidates = next_posting(candidates, inverted_index, candidates[0][0])
            for t in candidates:
                if t[1] >= c_pivot: break
                candidates = seek_to_document(candidates, inverted_index, t[0], c_pivot
                )
                candidates.sort(key=lambda x : x[1])
        print('Ans', Ans)
        print()

    return sorted(Ans, key=lambda x : x[0], reverse=True), full_eva_count

def DocInfo(candidates, term):
    for i in candidates:
        if i[0] == term:
            return i[1], i[2]

def next_posting(candidates, inverted_index, term):
    i = -1
    for j in range(len(candidates)):
        if candidates[j][0] == term:
            i = j
            break
    if i == -1: return candidates
    index = inverted_index[term].index((candidates[i][1], candidates[i][2]))
    if index+1 > len(inverted_index[term])-1:
        candidates.remove(candidates[i])
        return candidates
    next_p = inverted_index[term][index+1]
    candidates[i][1] = next_p[0]
    candidates[i][2] = next_p[1]
    return candidates

def seek_to_document(candidates, inverted_index, term, c_pivot):
    i = -1
    for j in range(len(candidates)):
        if candidates[j][0] == term:
            i = j
            break
    print('come on '*10, candidates, term, i)

    I_t = inverted_index[term]
    for c_t, w_t in I_t:
        if c_pivot <= c_t:
            candidates[i][1] = c_t
            candidates[i][2] = w_t
            break
        if I_t[-1] == (c_t, w_t):
            candidates.remove(candidates[i])
            break
    return candidates
