import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import os.path as op

#개체 각각의 적합도 계산
#리스트의 리스트 형식일 때 사용
def Erroreval(array):
    for j in range(0,len(array)):
        count = 0
        for i in range(0,50):
            if (array[j][1]*salmon[i][0]+array[j][2]*salmon[i][1]+array[j][3])>0:
                #salmon 분류 실패
                count +=1
            if (array[j][1]*seabass[i][0]+array[j][2]*seabass[i][1]+array[j][3])<0:
                #seabass 분류 실패
                count +=1
        #분류 실패한 수를 세서 반환
        array[j][0] = count 
    return array

#리스트 형식일 때 사용
def Erroreval_simple(array):
    count = 0
    for i in range(0,50):
        if (array[1]*salmon[i][0]+array[2]*salmon[i][1]+array[3])>0:
            #salmon 분류 실패
            count +=1
        if (array[1]*seabass[i][0]+array[2]*seabass[i][1]+array[3])<0:
            #seabass 분류 실패
            count +=1
    #분류 실패한 수를 세서 반환
    array[0] = count 
    return array
    
#Selection 의 가상룰렛은 배열로 만들어서 랜덤한 인덱스를 골라 선택하는 것으로 구현
#10% = 30, 20% = 25, 30% = 20, 40% = 7, 50% = 6, 60% = 5, 70% = 4, 80% = 1, 90% = 1, 100%= 1 의 비율로 1000개의 배열 생성
def Selection(array,num):
    random_selection = []
    for i in range(0,30):
        for j in range(0,10):
            random_selection.append(array[j])
        
    for i in range(0,25):
        for j in range(10,20):
            random_selection.append(array[j])
        
    for i in range(0,20):
        for j in range(20,30):
            random_selection.append(array[j])
        
    for i in range(0,7):
        for j in range(30,40):
            random_selection.append(array[j])
                        
    for i in range(0,6):
        for j in range(40,50):
            random_selection.append(array[j])
                
    for i in range(0,5):
        for j in range(50,60):
            random_selection.append(array[j])
                        
    for i in range(0,4):
        for j in range(60,70):
            random_selection.append(array[j])
                
    for i in range(70,80):
        random_selection.append(array[i])
                    
    for i in range(80,90):
        random_selection.append(array[i])
                    
    for i in range(90,100):
        random_selection.append(array[i])
    
    selection_array = []
    #교차 (전체 개체수 - 엘리트 개체수 - 뮤테이션개수) 개를 만들기위해선 그 두배를 선택해야한다
    #가상 룰렛을 만든곳에서 랜덤하게 뽑아서 배열을 생성한다
    for i in range(0,num*2): 
        selection_array.append(random_selection[random.randrange(0,1000)])
    
    return selection_array

#교차는 총 (전체 개체수 - 엘리트 개체수) 의 자식을 생성한다
def Crossover(array,num,mutProb):
    #1,2,3 이 파라미터니까 1~2사이 혹은 2~3사이를 한점으로 정해서 single potin crossover
    crossover_array = []
    tmp_x = 0
    tmp_y = 0
    tmp_z = 0
    n = num*2 -1
    for i in range(0,n):
        if(random.uniform(1,2) >= 1.5):
        # 1 과 2중에 랜덤으로 하나를 선택해서 1일경우
        # 그점을 중심으로 교차시킨다
            tmp_x = array[i][1]
            tmp_y = array[i+1][2]
            tmp_z = array[i+1][3]
        else:
            tmp_x = array[i][1]
            tmp_y = array[i][2]
            tmp_z = array[i+1][3]
        
        tmp = [0,tmp_x,tmp_y,tmp_z]
        
        # 랜덤값이 확률값보다 작을때 뮤테이션
        if(random.uniform(0,100) < mutProb*100):
            tmp = Mutation(tmp)
        tmp = Erroreval_simple(tmp)
        crossover_array.append(tmp)
        i +=1
        
    return crossover_array

#돌연 변이 생성
def Mutation(x):
    #각 파라미터를 50%확률로 랜덤값을 적용하게 된다
    if(random.uniform(1,2) >= 1.5):
        x[1] = random.uniform(-10.0,10.0)
    
    if(random.uniform(1,2) >= 1.5):
        x[2] = random.uniform(-10.0,10.0)
        
    if(random.uniform(1,2) >= 1.5):
        x[2] = random.uniform(-1000.0,1000.0)
        
    return x 

##### train 파일
#train 파일을 열어서 값단위로 읽어 배열생성
    
fd1 = open('salmon_train.txt','r')
salmon_t = fd1.readlines()
fd1.close()
salmon = []

for line in salmon_t:
    a = line.split()
    salmon.append([float(a[0]),float(a[1])])
    
fd2 = open('seabass_train.txt','r')
seabass_t = fd2.readlines()
fd2.close()
seabass = []

for line in seabass_t:
    a = line.split()
    seabass.append([float(a[0]),float(a[1])])

##### text 파일
fd1 = open('salmon_test.txt','r')
salmon_t = fd1.readlines()
fd1.close()
    
fd2 = open('seabass_test.txt','r')
seabass_t = fd2.readlines()
fd2.close()

salmon = []
seabass = []

#읽어들인 txt파일을 줄단위로 읽어들여서 list에 저장한다    
for line in salmon_t:
    a=line.split()
    salmon.append([float(a[0]),float(a[1])])

for line in seabass_t:
    a=line.split()
    seabass.append([float(a[0]),float(a[1])])

def runExp(popSize, elitNum, mutProb):
    print 'training...' #학습 서브루틴
    trResFn = 'train_log_%d_%d_%.2f' % (popSize,eliteNum,mutProb)
    
    #####################-학습 시작-#############################
    #log 를 입력하기 위한 파일 오픈
    f_name = '%s%d%s%d%s%.2f%s' %('train_log_',popSize,'_',elitNum,'_',round(mutProb,2),'.txt')
    fd_log = open(f_name,'w')

    genetic_array = []

    ##랜덤 염색체 부여
    for i in range(0,popSize):
        genetic_array.append([0,random.uniform(-10.0,10.0),random.uniform(-10.0,10.0),random.uniform(-1000,1000)])

    #1세대의 적합도 계산
    genetic_array = Erroreval(genetic_array)

    #랜덤 염색체들을 정렬한다 -> 엘리트들을 고르기위해
    genetic_array.sort()
    #가장 좋은 염색체의 오류율을 저장해둔다
    low_e = genetic_array[0][0]   

    count = 1
    
    print('%d%s%f%s%f%s%f' % (count,'th elit parameter =>', genetic_array[0][1],'  ',genetic_array[0][2],'   ',genetic_array[0][3]))
    print('%s%d' % ('the lowest error = ',low_e))
    fd_log.write('%s%d%s%d%s' % ('count = ',count,'the lowest error = ',low_e,'\n'))
    fd_log.write('%d%s%f%f%f%s' % (count,'세대 엘리트 개체 파라미터 =>', genetic_array[0][1],genetic_array[0][2],genetic_array[0][3],'\n'))
    #학습은 오류율이 9%이하로 떨어지면 중단한다
    while(low_e>8):    
        count += 1
        
        #선택을 통해서 가상의 룰렛을 만들어 뽑은 염색체를 교차시킨다
        child_array = []
        child_array = Selection(genetic_array,popSize)
        child_array = Crossover(child_array,popSize,mutProb)
        
        #좋은 부모개체 elitNum개는 다음세대에 그대로 물려준다
        elitism_array = []
        for i in range(0,elitNum):
            elitism_array.append(genetic_array[i])
                
        #다음 세대 염색체를 리스트로 합친다
        genetic_array = []
        genetic_array.extend(child_array)
        genetic_array.extend(elitism_array)
        
        genetic_array.sort()
        low_e = genetic_array[0][0]
        print('%d%s%f%s%f%s%f' % (count,'th elit parameter =>', genetic_array[0][1],'  ',genetic_array[0][2],'   ',genetic_array[0][3]))
        print('%s%d' % ('the lowest error = ',low_e))
        fd_log.write('%s%d%s%d%s' % ('count = ',count,'the lowest error = ',low_e,'\n'))
        fd_log.write('%d%s%f%f%f%s' % (count,'세대 엘리트 개체 파라미터 =>', genetic_array[0][1],genetic_array[0][2],genetic_array[0][3],'\n'))
    
    fd_log.close()
    
    print 'result file:' ,trResFn
    print 'testing...' #테스트 서브루틴
    #####################-테스트 시작-#####################################
    # train을 통해 학습한 prameter값을 세팅
    # 훈련된 염색체 중 가장 상위 염색체의 파라미터 값으로 설정
    tmp_x=genetic_array[0][1]
    tmp_y=genetic_array[0][2]
    tmp_z=genetic_array[0][3]
    parameter = [tmp_x,tmp_y,tmp_z]
    x_coefficient = -(parameter[0]/parameter[1])
    x_constant =(parameter[2]/parameter[1])
         
    #출력값 저장하기위한 txt파일 오픈
    f_name = '%s%d%s%d%s%.2f%s' %('test_output_',popSize,'_',elitNum,'_',round(mutProb,2),'.txt')
    fd3 = open(f_name,'w')
    
    #이 배열들은 그림으로 분류결과를 나타내기 위해 관리한다
    c_salmon = []
    m_salmon = []
    c_seabass = []
    m_seabass = []
    
    #분류시작, 출력 결과를 txt파일에 적는다
    #이때, 그림으로 분류성공과 분류실패를 나타내기위해서 성공했을때와 실패했을때를 분류해서 list에 저장해둔다
    for i in range(0,50):
        if (parameter[0]*salmon[i][0]+parameter[1]*salmon[i][1]+parameter[2])>0:
            #분류실패
            fd3.write('%s%d%s%d%s' %('salmon =',salmon[i][0],', ',salmon[i][1],' =>  fail\n'))
            m_salmon.append(salmon[i])
        else:
            #분류성공
            fd3.write('%s%d%s%d%s' %('salmon =',salmon[i][0],', ',salmon[i][1],' =>  correct\n'))
            c_salmon.append(salmon[i])
            
    for i in range(0,50):        
        if (parameter[0]*seabass[i][0]+parameter[1]*seabass[i][1]+parameter[2])<0:
            #분류실패
            fd3.write('%s%d%s%d%s' %('seabass =',seabass[i][0],', ',seabass[i][1],' =>  fail\n'))
            m_seabass.append(seabass[i])
        else:
            #분류성공
            fd3.write('%s%d%s%d%s' %('seabass =',seabass[i][0],', ',seabass[i][1],' =>  correct\n'))
            c_seabass.append(seabass[i])
            
    #위에서 계산한 결과로 error율을 저장해둔다
    errorrate = (len(m_salmon)+len(m_seabass))*0.01
    fd3.write('%s%f' % ('errorrate => ',errorrate))

    f_name = '%s%d%s%d%s%.2f%s' %('test_output_',popSize,'_',elitNum,'_',mutProb,'.png')
    print('%s%f' % ('test errorrate => ',errorrate))
    if __name__ == '__main__':
        fig, ax = plt.subplots()
        
        xList = []
        yList = []
        
        #분류성공한 salmon은 초록색삼각형으로 그린다
        for data in c_salmon:
            x,y = data
            xList.append(x)
            yList.append(y)
        ax.plot(xList,yList,'g^',Label='salmon')
        
        xList = []
        yList = []
        
        #분류성공한 seabass는 노란색사각형으로 그린다
        for data in c_seabass:
            x,y = data
            xList.append(x)
            yList.append(y)
        ax.plot(xList,yList,'ys',Label='seabass')
        
        xList = []
        yList = []
        
        #분류실패한 salmon은 빨간색삼각형으로 그린다
        for data in m_salmon:
            x,y = data
            xList.append(x)
            yList.append(y)
        ax.plot(xList,yList,'r^',Label='salmon')
        
        xList = []
        yList = []
        
        #분류실패한 seabass는 빨간색사각형으로 그린다
        for data in m_seabass:
            x,y = data
            xList.append(x)
            yList.append(y)
        ax.plot(xList,yList,'rs',Label='seabass')
        
        ax.grid(True)
        ax.legend(loc='upper right')
        ax.set_xlabel('Length of body')
        ax.set_ylabel('Length of tail')
        ax.set_xlim((None,None))
        ax.set_ylim((None,None))
        
        #분류자를 빨간색 점선으로 그린다
        a = np.arange(0.0,120.0,0.01)
        ax.plot(a,x_coefficient*a-x_constant,'r--')
        
        plt.savefig(f_name)
        plt.show()
        
    fd3.close()
    tsResFn = 'test_output_%d_%d_%.2f' % (popSize,elitNum,mutProb)
    print 'result file: ',tsResFn
    
if __name__ == '__main__':
    argmentNum = len(sys.argv)
        
    if argmentNum == 4: #command line argument 수 확인
        popSize = int(sys.argv[1])  # 전체 개체 수
        eliteNum = int(sys.argv[2]) # elite 개체 수
        mutProb = float(sys.argv[3])# mutation 확률
        runExp(popSize,eliteNum,mutProb)
    else :
        print('Usage: %s [populationSize] [eliteNum] [mutatonProb]') % (op.basename(sys.argv[0]))
