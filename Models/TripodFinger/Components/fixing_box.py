__authors__ = "tnavez, qpeyron"
__contact__ = "tanguy.navez@inria.fr, quentin.peyron@inria.fr"
__version__ = "1.0.0"
__copyright__ = "(c) 2020, Inria"
__date__ = "Feb 09 2023"

from splib3.objectmodel import SofaPrefab
from splib3.numerics import getOrientedBoxFromTransform


class FixingBox(SofaPrefab):
    """Fix a set of 'dofs' according to a translation & orientation"""

    def __init__(self, parent, target, name='FixingBox',
                 translation=[0.0, 0.0, 0.0], eulerRotation=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0]):

        ob = getOrientedBoxFromTransform(translation=translation, eulerRotation=eulerRotation, scale=scale)

        self.node = parent.addChild(name)
        self.node.addObject('BoxROI',
                               orientedBox=ob,
                               name='BoxROI',
                               position=target.dofs.getData('rest_position').getLinkPath(),
                               drawBoxes=False)

        c = self.node.addChild('Constraint')
        target.addChild(c)

        c.addObject('RestShapeSpringsForceField',
                       indices=self.node.BoxROI.getData('indices').getLinkPath(),
                       stiffness=1e12)
