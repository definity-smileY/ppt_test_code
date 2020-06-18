from fapp.IClass import IClassName
from fapp.IClassOtP import IClassOtParent


class ClassChildCMParent_I(IClassName, IClassOtParent):
    # 어트리뷰트
    vChildMParent = 888


    # 초기화 비헤비어
    def __init__(self, pParent1, pParent2):
        # 상속초기화
        IClassName.__init__(self, pParent1)
        IClassOtParent.__init__(self, pParent2)

    # 비헤비어
    def testChildMParentI():
        return 'testChildMParentI의 메세지'

    # 첫번째 부모클래스에게 상속받은 함수 구현
    def testParentI():
        return 'IClassName의 메세지'

    # 두번째 부모클래스에게 상속받은 함수 구현
    def testOtParent():
        return 'IClassOtP의 메세지'