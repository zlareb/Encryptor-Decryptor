
def get_permutations(sequence):
    '''
    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    '''

    if len(sequence) == 1: 
        return [sequence]
    else: 
        result = []
        perms = get_permutations(sequence[1:])
        for perm in perms:
            for i in range(len(perm)+1):
                result.append(perm[:i] + sequence[0] + perm[i:])
        return result

            

if __name__ == '__main__':

   findperm = input("Please enter the string that you want to find the permutations of: ")
   print("The permutations are as follows:", get_permutations(findperm))
    


