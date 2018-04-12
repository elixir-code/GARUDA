===============================
GARUDA - Sharp | Swift | Strong
===============================

Visual Inspection of Mechanical Components in the Assembly line using Computer Vision


Running the Program
-------------------

To run the application, execute the ``gui_home.py`` script located in the ``GARUDA/gui`` directory ::

	$ python3 GARUDA/gui/gui_home.py

.. note:: The application works only with **live camera feeds**. Use URL **'0'** to access the **in-built camera** in laptops or **'1'** (or higher numbers) to access **external USB webcams**. Alternatively, you can also specify the IP address of an IP Camera connected on the network.


Dependencies
------------

The application is written in ``Python3`` using standard image and numerical processing libraries.

**Image Processing :** OpenCV, Numpy

**GUI Design :** PyQt5