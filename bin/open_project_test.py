import winlogtimeline.util

def main():
    proj_path = 'TestProject'
    project = winlogtimeline.util.project.Project(proj_path)
    project.close()


if __name__ == '__main__':
    main()
