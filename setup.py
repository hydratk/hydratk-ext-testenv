from distutils.core import setup


with open("README.md", "r") as f:
    readme = f.readlines()
    
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",
    "Framework :: HydraTk",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",    
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",    
    "Programming Language :: Python :: Implementation :: PyPy",    
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
];

packages=[
          'hydratk.extensions.testenv', 
         ];
                
setup(name='Hydratk-TestEnv',
      version='0.1.0',
      description='Test environmanet for test automation exercises',
      long_description=readme,
      author='Petr Rašek',
      author_email='pr@hydratk.org',
      url='http://www.hydratk.org',
      license='BSD',
      packages=packages,
      package_dir={'' : 'src'},
      classifiers=classifiers
     )