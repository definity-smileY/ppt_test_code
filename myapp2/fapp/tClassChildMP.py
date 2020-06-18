from fapp.tClass import tClassName
from fapp.tClassOtP import tClassOtParent

class tClassChildCMParent(tClassName,tClassOtParent):
    # 어트리뷰트
    vChildMParent = 888

    # 초기화 비헤비어
    # def__init__(self,부모클래스매개변수목록.....):
    def __init__(self, pParent1, pParent2):
        #상속초기화
        tClassName.__init__(self, pParent1)
        tClassOtParent.__init__(self, pParent2)

    # 비헤비어
    def testChildMParent():
        a = 2
        b = 10
        return b-a