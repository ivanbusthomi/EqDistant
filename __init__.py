# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EqDistant
                                 A QGIS plugin
 This plugin creates equidistant line
                             -------------------
        begin                : 2014-12-08
        copyright            : (C) 2014 by Ivan Busthomi
        email                : ivanbusthomi@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load EqDistant class from file EqDistant.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .eq_distant import EqDistant
    return EqDistant(iface)
