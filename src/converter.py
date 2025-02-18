import os
import glob
import datetime as dt
class MCAtoOxfordConverter:
    def __init__(self, folder_path):
        self.folder_path = folder_path
    
    def read_mca_file(self, file_path):
        mcadat = {}
        
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            content = f.read()
            
        lines = content.split('\n')
        
        liveTimeIdx = [i for i, line in enumerate(lines) if 'LIVE_TIME' in line][0]
        realTimeIdx = [i for i, line in enumerate(lines) if 'REAL_TIME' in line][0]
        dataStartIdx = [i for i, line in enumerate(lines) if '<<DATA>>' in line][0]
        dataEndIdx = [i for i, line in enumerate(lines) if '<<END>>' in line][0]
        dateTimeIdx = [i for i, line in enumerate(lines) if 'START_TIME' in line][0]
        
        tempArray = lines[liveTimeIdx].strip().split(" ")
        mcadat['livetime'] = float(tempArray[-1])
        
        tempArray = lines[realTimeIdx].strip().split(" ")
        mcadat['realtime'] = float(tempArray[-1])
        
        tempArray = lines[dateTimeIdx].strip().split(" ")
        datestring = f"{tempArray[-2]} {tempArray[-1]}"

        mcadat['datetime'] = dt.datetime.strptime(datestring,"%m/%d/%Y %H:%M:%S")
        
        countTemp = [int(x) for x in lines[dataStartIdx + 1:dataEndIdx]]
        mcadat['counts'] = countTemp
        mcadat['channels'] = len(countTemp)
        mcadat['totalCounts'] = sum(countTemp)
        return mcadat

    def write_oxford_file(self,mca_data, output_path):
        theDT = mca_data['datetime']
        seconds2Midnight = theDT.hour*3600 + theDT.minute*60 + theDT.second
        header = ['4096,1\n', mca_data['datetime'].strftime("%Y, %j,") + str(seconds2Midnight) +','+ str(mca_data['realtime']) + ',' + str(mca_data['totalCounts']) + ',"\n']
        core =  [str(count) + ',\n' for count in mca_data['counts']]
        output = header + core
        o = open(output_path,'w')
        o.writelines(output)
        o.close()
    
    def convert_folder(self):
        mca_files = glob.glob(os.path.join(self.folder_path, "*.mca"))
        
        for file_path in mca_files:
            mca_data = self.read_mca_file(file_path)
            
            output_path = os.path.splitext(file_path)[0] + ".dat"
            self.write_oxford_file(mca_data, output_path)

    def find_dat_files(self, directory):
        try:
            with open(os.path.join(directory, "00_nameList.txt"), 'w') as f:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.endswith('.dat'):
                            full_path = os.path.join(root, file)
                            f.write(full_path + '\n')
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    folder_path = "/Users/tm98/Downloads/10.12.23" 
    converter = MCAtoOxfordConverter(folder_path)
    converter.convert_folder()



