""" shared functions to manage Jfrog Platform """


def setlayout(ptype):
    ''' Choose the correct default layout based on the repository type '''
    specialtypes = ['bower', 'cargo', 'composer', 'conan', 'go', 'ivy',
                    'npm', 'nuget', 'puppet', 'sbt', 'swift', 'vcs']
    if ptype.lower() in ['maven', 'gradle']:
        return 'maven-2-default'
    if ptype.lower() in specialtypes:
        return ptype.lower() + '-default'
    return 'simple-default'
