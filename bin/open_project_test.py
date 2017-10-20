import winlogtimeline.util
import os


def main():
    proj_path = os.path.join(winlogtimeline.util.data.get_appdir(), 'TestProject')
    project = winlogtimeline.util.project.Project(proj_path)
    project.close()


if __name__ == '__main__':
    main()
