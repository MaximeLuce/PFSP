import numpy as np

class DataLoader:
    """
    Utilitary to read and extract the data
    Input: a .fsp file for a specific problem
    Output: - num_jobs ; number of jobs J of the problem
            - num_machines ; number of machines M of the problem
            - processing_times ; matrixe M x J of the time of each job on each machine
    """
    
    @staticmethod
    def load_from_file(filepath):
        with open(filepath, 'r') as file: # open the file
            lines = file.readlines() # get the lines
        
        # we clean the input by removing space and empty
        lines = [line.strip() for line in lines if line.strip()]
        
        # first line contains paramets title: num_jobs, num_machines, seed, upper_bound, lower_bound
        params = lines[1].split()
        num_jobs = int(params[0])
        num_machines = int(params[1])
        
        # the matrix of "processing times" starts after this line
        # we get the indice of that line
        start_idx = 0
        for i, line in enumerate(lines):
            if "processing times" in line:
                start_idx = i + 1
                break
                
        # extract the matrix of processing time
        processing_times = []

        all_numbers = []
        for line in lines[start_idx:]: # we start after the line with "processing times"
            all_numbers.extend([int(x) for x in line.split()])
            
        # we construct the matrix of size M x J
        for m in range(num_machines):
            row = all_numbers[m * num_jobs : (m + 1) * num_jobs]
            processing_times.append(row)
            
        return num_jobs, num_machines, np.array(processing_times)
    
# TEST
'''
e = Emprunt(3,5)
print(e)

print(e.get_numero_lecteur())
print(e.get_numero_livre())
print(e.get_date())
'''