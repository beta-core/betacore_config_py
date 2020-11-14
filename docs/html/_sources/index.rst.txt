.. betacore configuration documentation master file, created by
   sphinx-quickstart on Sat Nov 14 09:48:43 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Getting started
======================

Welcome to betacore configuration's documentation!

The objective is to move out some settings for python application into configuration file(s).
:const:`EnvironmentAdapter` allows for simple conversion of environment variables.

This allows yaml with `text: ${ENV_VAR}` to be replaced with `text: cool` assuming
`ENV_VAR` is environment variables with the value of cool




Installation
------------------
`pip3 install betacore_config`


Usage
---------

Command
^^^^^^^^^
.. highlight:: shell
.. code-block:: shell

   export TEST_ENV='some text'
   python3 sample.py --config test.yml

sample.py
^^^^^^^^^
.. highlight:: python
.. code-block:: python
   :linenos:


   import argparse
   from betacore.config import YamlConfiguration

   def main()

      parser = argparse.ArgumentParser(description='Process some integers.')
      parser.add_argument('--config', type=str, help='configuration file location')
      args, _ = parser.parse_known_args()


      config = YamlConfiguration(args.config)
      # Note this will be the first section of the yml file
      #      a section is split up by using: ---
      data: dict = config.config()
      print(data)

   if __name__ == '__main__':
      main()

test.yml
^^^^^^^^^
.. highlight:: yaml
.. code-block:: yaml
   :linenos:

   ---

   test:
   list:
      - a
      - b
      - c
   env:
      environment_variable: 'TEST_ENV'
   level:
      two:
         a: a


Classes
==================================================

.. automodule:: betacore.config.config
    :members:
    :undoc-members:
    :show-inheritance:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
