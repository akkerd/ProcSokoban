class Generator:
    templates = []
    wildcards = []

    def __init__(self, key_templates, wildcards = []):
        Generator.templates = key_templates
        Generator.wildcards = wildcards

    def getlevel(self, size=[2,2]):
        # Generate the grid
        templategrid = [ [ None for i in range(size[0]) ] for j in range(size[1]) ]
        # templategrid = {}
        print("Empty template grid",templategrid)
        print("Templates: ",Generator.templates)

        templategrid[0][0] = Generator.templates[0].OriginalLevel
        templategrid[0][1] = Generator.templates[1].OriginalLevel
        templategrid[1][0] = Generator.templates[2].OriginalLevel
        templategrid[1][1] = Generator.templates[3].OriginalLevel

        # Create final level
        lastRow = 0
        outGrid = {}
        for templateRowCount, templateRow in enumerate(templategrid):
            for templateCount, template in enumerate(templateRow):
                for rowCount, row in enumerate(template):
                    if rowCount + lastRow in outGrid:
                        outGrid[rowCount + lastRow] = outGrid[rowCount + lastRow] + row
                    else:
                        outGrid[rowCount + lastRow] = row
            lastRow += len(template)
        return outGrid
