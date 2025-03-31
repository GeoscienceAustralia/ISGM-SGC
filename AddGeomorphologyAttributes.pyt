#### Author: Zhi Huang Organisation: Geoscience Australia Email:
#### Zhi.Huang@ga.gov.au Date: August 15, 2022 Python version: 3+ ArcGIS
#### Pro: 2.6.4 and above

import arcpy
from arcpy import env
from arcpy.sa import *
import numpy as np
arcpy.CheckOutExtension("Spatial")


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "AddAttributes"

        # List of tool classes associated with this toolbox
        # There is only one tool. The tool add a list of geomorphology attributes to the selected features of the active layer in the active map in ArcGIS Pro.
        self.tools = [Add_Geomorphology_Attributes_Tool]



class Add_Geomorphology_Attributes_Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Add Geomorphology Attributes Tool"
        self.description = "Add Geomorphology Attributes to the selected features"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # first parameter
        param0 = arcpy.Parameter(
            displayName="Input Features",
            name="inFeatClass",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        
        # second parameter
        param1 = arcpy.Parameter(
            displayName="Output Features",
            name="outFeatClass",
            datatype="DEFeatureClass",
            parameterType="Derived",
            direction="Output")
        param1.parameterDependencies = [param0.name]

        # third parameter
        param2 = arcpy.Parameter(
            displayName="Physiography Setting",
            name="physiograpy",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param2.filter.type = "ValueList"
        # Table 17-1 Physiography in Part 2 Geomorphology Scheme (Nanson et al., 2023)
        param2.filter.list = ['NA'] + sorted(['Continental Shelf','Continental Slope','Continental Rise','Oceanic Trench','Mid-ocean Ridge',
                      'Axial Valley','Axial High','Abyssal Plain','Accretionary Prism','Back-arc Basin','Fore-arc Basin','Island Arc'])
        param2.value = 'NA'
        
        # 4th parameter
        param3 = arcpy.Parameter(
            displayName="Geomorphology Setting or Process",
            name="setting_process",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param3.filter.type = "ValueList"
        param3.filter.list = ['NA','Unknown'] + sorted(['Fluvial','Coastal','Marine','Glacial','Solid Earth',
                      'Current-induced','Biogenic','Mass Movement','Fluid Flow','Karst','Anthropogenic'])
        param3.value = 'NA'

        # 5th parameter
        param4 = arcpy.Parameter(
            displayName="Basic geomorphic unit (BGU)",
            name="BGU",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param4.filter.type = "ValueList"
        param4.filter.list = ['NA','Unknown']
        param4.value = 'NA' # default value

        # 6th parameter
        param5 = arcpy.Parameter(
            displayName="BGU Type (BGU-T)",
            name="BGU_T",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param5.filter.type = "ValueList"
        param5.filter.list = ['NA','Unknown']
        param5.value = 'NA'

        # 7th parameter
        param6 = arcpy.Parameter(
            displayName="BGU sub-Type (BGU-sT)",
            name="BGU_sT",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param6.filter.type = "ValueList"
        param6.filter.list = ['NA','Unknown']
        param6.value = 'NA'

        # 8th parameter
        param7 = arcpy.Parameter(
            displayName="Additional process attribute",
            name="process",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param7.filter.type = "ValueList"
        param7.filter.list = ['NA']
        param7.value = 'NA'

        # 9th parameter
        param8 = arcpy.Parameter(
            displayName="Additional geometric attribute",
            name="geometric",
            datatype="GPString",
            parameterType="Required",
##            multiValue=True,
            direction="Input")
        param8.filter.type = "ValueList"
        param8.filter.list = ['NA']
        param8.value = 'NA'

        # 10th parameter
        param9 = arcpy.Parameter(
            displayName="Group of units",
            name="group",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param9.filter.type = "ValueList"
        param9.filter.list = ['NA','chain','field']
        param9.value = 'NA'

        # 11th parameter
        param10 = arcpy.Parameter(
            displayName="Relative age",
            name="age",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param10.filter.type = "ValueList"
        param10.filter.list = ['NA'] + sorted(['relict','palimpsest','modern'])
        param10.value = 'NA'

        # 12th parameter
        param11 = arcpy.Parameter(
            displayName="Stratigraphic position",
            name="stratigraphic",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param11.filter.type = "ValueList"
        param11.filter.list = ['NA'] + sorted(['surface','buried','partially buried'])
        param11.value = 'NA' 


        # 13th parameter
        param12 = arcpy.Parameter(
            displayName="Relative sea level",
            name="sealevel",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param12.filter.type = "ValueList"
        param12.filter.list = ['NA'] + sorted(['transgressive','regressive','stillstand'])
        param12.value = 'NA'


        # 14th parameter
        param13 = arcpy.Parameter(
            displayName="Lithology",
            name="lithology",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param13.filter.type = "ValueList"
        param13.filter.list = ['NA'] + sorted(['hard','soft sediment (siliciclastic or carbonate)','consolidated sediment'])
        param13.value = 'NA'


        # 15th parameter
        param14 = arcpy.Parameter(
            displayName="Particle size characterisation",
            name="particleSize",
            datatype="GPValueTable",
            parameterType="Required",
            direction="Input")
        param14.columns = [['GPString','Value'],['GPString','Unit']]
        param14.filters[1].type = "ValueList"
        param14.values = [['9999','mm']]       
        param14.filters[1].list = ['mm','phi']        
 

        # 16th parameter
        param15 = arcpy.Parameter(
            displayName="Terrain attribute",
            name="terrain",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param15.value = 'NA'

        # 17th parameter
        param16 = arcpy.Parameter(
            displayName="Marginal marine process classification",
            name="marginal",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param16.filter.type = "ValueList"
        # this does not work because could not get Python to display Italic character in a text string
##        param16.filter.list = ['NA','F','W','T','Fw',
##                               'Ft','Tf','Tw',
##                               'Wt','Wf','Fw' + '\u0054',
##                               'Fluvial dominated, tide influenced, wave affected','Tide dominated, fluvial influenced, wave affected',
##                               'Tide dominated, wave influenced, fluvial affected','Wave dominated, tide influenced, fluvial affected',
##                               'Wave dominated, fluvial influenced, tide affected','fw','tf',
##                               'wt','fwt','Fwt',
##                               'Twf','Wtf']
        param16.filter.list = ['NA'] + sorted(['Fluvial dominated','Wave dominated','Tide dominated','Fluvial dominated, wave influenced',
                               'Fluvial dominated, tide influenced','Tide dominated, fluvial influenced','Tide dominated, wave influenced',
                               'Wave dominated, tide influenced','Wave dominated, fluvial influenced','Fluvial dominated, wave influenced, tide affected',
                               'Fluvial dominated, tide influenced, wave affected','Tide dominated, fluvial influenced, wave affected',
                               'Tide dominated, wave influenced, fluvial affected','Wave dominated, tide influenced, fluvial affected',
                               'Wave dominated, fluvial influenced, tide affected','fluvial and wave influenced','tide and fluvial influenced',
                               'wave and tide influenced','fluvial, wave and tide influenced','Fluvial dominated, wave and tide influenced',
                               'Tide dominated, wave and fluvial influenced','Wave dominated, tide and fluvial influenced'])
        param16.value = 'NA'

        # 18th parameter
        param17 = arcpy.Parameter(
            displayName="Aeolian input",
            name="aeolian",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param17.filter.type = "ValueList"
        param17.filter.list = ['NA','aeolian']
        param17.value = 'NA'

        # 19th parameter
        param18 = arcpy.Parameter(
            displayName="Comments",
            name="comments",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        param18.value = 'NA'

        # 20th parameter
        param19 = arcpy.Parameter(
            displayName="Geomorphology analyst name",
            name="operator",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        # 21th parameter
        param20 = arcpy.Parameter(
            displayName="Geomorphology analyst organisation",
            name="organisation",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param20.value = 'Geoscience Australia'

        
        parameters = [param0, param1, param2, param3, param4, param5, param6,param7,param8,param9,param10,
                      param11,param12,param13,param14,param15,param16,param17,param18,param19,param20]
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        helper = helpers()
        # key bits of the tool
        # basically we want to update the drop-down lists based on certain selections
        if parameters[3].value:
            if parameters[3].value == 'Current-induced':
                parameters[4].filter.list = ['NA','Unknown'] + sorted(['current-induced channel','chute channel',
                                             'oxbow','plunge pool','knickpoint','bedform','barform'])
                # the following two lists are available only when the 'Current-induced" setting is selected
                parameters[7].filter.list = ['NA'] + sorted(['erosional','accretionary/aggradational','unidirectional flow',
                                             'bidirectional flow','interference','constrained flow','open flow',
                                             'tidal current','turbidity current','density current'])
                parameters[8].filter.list = ['NA'] + sorted(['2D','3D','primary','secondary','compound','longitudinal',
                                             'transverse','oblique','straight crests','sinuous crests',
                                             'linguoid crests','lunate crests','crescent'])
                helper.do_current_induced(parameters)
            elif parameters[3].value == 'Coastal':
                parameters[4].filter.list = ['NA','Unknown'] + sorted(['coastal subaerial valley','floodplain terrace','channel ledge',
                                             'floodplain','coastal delta','delta lobe','channel belt','subaerial channel',
                                             'barrier complex','barrier system','barrier','beach ridge','chenier ridge',
                                             'beachface','foreshore','shoreface','back barrier','tidal flat','lagoon',
                                             'beach','raised beach','rocky coast','coastal barform',
                                             'current-induced channel','chute channel','oxbow','plunge pool',
                                             'knickpoint','bedform','barform'])
                # the Coastal, Marine and Fluvial settings include the Current-induced setting.
                # The update of the param7 and param8 occur in the corresponding do_ functions.
                helper.do_coastal(parameters)                
            elif parameters[3].value == 'Fluvial':
                parameters[4].filter.list = ['NA','Unknown'] + sorted(['drainage basin','catchment','drainage network',
                                             'fluvial fan','fluvial fan lobe','fluvial subaerial valley','floodplain terrace',
                                             'channel ledge','floodplain','fluvial delta','delta lobe','channel belt',
                                             'subaerial channel','current-induced channel','chute channel','oxbow',
                                             'plunge pool','knickpoint','bedform','barform'])

                helper.do_fluvial(parameters)
            elif parameters[3].value == 'Marine':
                parameters[4].filter.list = ['NA','Unknown'] + sorted(['marine barform','submarine channel',
                                             'submarine channel belt','submarine gully','submarine valley',
                                             'canyon mouth','canyon head','submarine canyon',
                                             'submarine tributary canyon','submarine fan-valley','submarine fan',
                                             'submarine terrace','marine reef','current-induced channel','chute channel',
                                             'oxbow','plunge pool','knickpoint','bedform','barform'])

                helper.do_marine(parameters)                
            elif parameters[3].value == 'Glacial':
                parameters[4].filter.list = ['NA','Unknown'] + sorted(['U-shaped valley','cross-shelf trough','glacial fjord',
                                             'sill/threshold','glacial basin','streamlined landform','Rogen (ribbed) moraine',
                                             'meltwater channel','tunnel valley','glacitectonic raft',
                                             'thrust-block moraine','cupola hill','hill-hole pair','medial moraine',
                                             'crevasse-filling','crevasse-squeeze ridge','erratic','esker','moraine',
                                             'hummocky terrain','grounding zone wedge','ice-proximal fan',
                                             'grounding-line fan','grounding zone fan','ice-contact fan',
                                             'corrugation ridges','ribs','sub-ice shelf keel scour mark',
                                             'glacigenic debris flow/lobe','trough-mouth fan','ice-contact delta',
                                             'iceberg ploughmark','iceberg grounding pit',
                                             'corrugation ridges within ploughmarks','kettle hole',
                                             'proglacial meltwater channel','glacifluvial delta','glacier-fed delta',
                                             'glacifluvial outwash plain','sandur'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']

                helper.do_glacial(parameters)     
            elif parameters[3].value == 'Solid Earth':
                parameters[4].filter.list = ['NA','Unknown'] + sorted(['guyot','oceanic core complex','axial volcanic ridge',
                                             'abyssal hill','volcano (island or submarine)','astrobleme','impact crater',
                                             'bedrock outcrop (undefined)','magmatic outcrop','tectonic depression',
                                             'tectonic high','bedding ridge','dip slope','bench','scarp slope','cliff',
                                             'tectonic lineament','tectonic escarpment'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']

                helper.do_solidEarth(parameters)
            elif parameters[3].value == 'Biogenic':
                parameters[4].filter.list = ['NA','Unknown'] + sorted(['biogenic reef','fore-reef','reef crest','reef flat','back reef',
                                             'reef lagoon','spur-and-groove','sediment apron','biostrome','bed',
                                             'bioherm','mound','mat','excavation'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']

                helper.do_biogenic(parameters)    
            elif parameters[3].value == 'Mass Movement':
                parameters[4].filter.list = ['NA','Unknown'] + sorted(['fall','topple','slide','flow','lateral spread','complex',
                                             'evacuation zone','headwall domain','depletion zone','extensional domain',
                                             'depositional zone','accumulation zone','compressional domain',
                                             'talus apron','debris apron','remnant block','translated block',
                                             'mudflow gully','turbidity channel','crown crack','tension cracks',
                                             'transverse crack','head scarp','headwall','lateral scarp','sidewall',
                                             'minor scarp','secondary escarpment','talus fan','debris fan','mudflow fan',
                                             'turbidite fan','mass-movement toe','extensional ridge','mass-movement compressional ridge',
                                             'transverse ridge','turbidite levee'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']

                helper.do_massMovement(parameters)    
            elif parameters[3].value == 'Fluid Flow':
                parameters[4].filter.list = ['NA','Unknown'] + sorted(['hydrothermal vent','hydrothermal mound','mud volcano',
                                             'caldera (mud volcano)','crater','gryphon (mud volcano)',
                                             'moat (mud volcano)','subsidence rim','mudflow (mud volcano)','ring fault',
                                             'outcropping methane-derived authigenic carbonate (MDAC)',
                                             'pingo','blow-out crater','permafrost pingo depression ','pockmark'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']

                helper.do_fluidFlow(parameters)
            elif parameters[3].value == 'Karst':
                parameters[4].filter.list = ['NA','Unknown'] + sorted(['carbonate karst','salt karst','sandstone karst'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
                helper.do_karst(parameters)
            elif parameters[3].value == 'Anthropogenic':
                parameters[4].filter.list = ['NA','Unknown'] + sorted(['archaeological','structure','disturbance'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
                helper.do_anthropogenic(parameters)
            else:
                parameters[4].filter.list = ['NA','Unknown']
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
                
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        inFeatClass = parameters[0].valueAsText
        outFeatClass = parameters[1].valueAsText
 
        
        # calling the helper functions
        helper = helpers()
        inFeatClass = helper.convert_backslash_forwardslash(inFeatClass)

        # if the input feature class is selected from a drop-down list, the inFeatClass does not contain the full path
        # In this case, the full path needs to be obtained from the map layer
        if inFeatClass.rfind("/") < 0:
            aprx = arcpy.mp.ArcGISProject("CURRENT")
            m = aprx.activeMap            
            for lyr in m.listLayers():
                if lyr.isFeatureLayer:
                    if inFeatClass == lyr.name:
                        inFeatClass = helper.convert_backslash_forwardslash(lyr.dataSource)
                        break; #get the active layer and exit
        

       # check that the input feature class is in a correct format
        vecDesc = arcpy.Describe(inFeatClass)
        vecType = vecDesc.dataType        
        if (vecType != 'FeatureClass') or (inFeatClass.rfind(".gdb") == -1):
            messages.addErrorMessage("The input featureclass must be a feature class in a File GeoDatabase!")
            raise arcpy.ExecuteError
        

        
        workspaceName = inFeatClass[0:inFeatClass.rfind("/")] 
        env.workspace=workspaceName
        env.overwriteOutput = True

        # get the values enter/select by the user
        valueList = []
        physiography = parameters[2].valueAsText
        valueList.append(physiography)        
        setting_process = parameters[3].valueAsText
        valueList.append(setting_process)
        BGU = parameters[4].valueAsText
        valueList.append(BGU)
        BGU_T = parameters[5].valueAsText
        valueList.append(BGU_T)
        BGU_sT = parameters[6].valueAsText
        valueList.append(BGU_sT)
        process = parameters[7].valueAsText
        valueList.append(process)
        geometric = parameters[8].valueAsText
        valueList.append(geometric)
        group = parameters[9].valueAsText
        valueList.append(group)
        age = parameters[10].valueAsText
        valueList.append(age)
        stratigraphic = parameters[11].valueAsText
        valueList.append(stratigraphic)
        sealevel = parameters[12].valueAsText
        valueList.append(sealevel)
        lithology = parameters[13].valueAsText
        valueList.append(lithology)
        particleSize = parameters[14].valueAsText
        if particleSize == '9999 mm':
            particleSize = 'NA' # default value
        else:
            pSV = particleSize.split(' ')[0]
            pSU = particleSize.split(' ')[1]
            if not helper.is_number(pSV):
                messages.addErrorMessage("The value for the particle size must be a valid number!")
                raise arcpy.ExecuteError
            elif (pSU == 'mm') and (float(pSV) <= 0):
                messages.addErrorMessage("It is not valid to have a negative particle size in mm unit!")
                raise arcpy.ExecuteError
        valueList.append(particleSize)
        terrain = parameters[15].valueAsText
        valueList.append(terrain)
        marginal = parameters[16].valueAsText
        valueList.append(marginal)
        aeolian = parameters[17].valueAsText
        valueList.append(aeolian)
        comments = parameters[18].valueAsText
        valueList.append(comments)
        operator = parameters[19].valueAsText
        valueList.append(operator)
        organisation = parameters[20].valueAsText
        valueList.append(organisation)

        
        # display the number of selected feature for the active layer
        result = arcpy.GetCount_management(lyr)
        arcpy.AddMessage(result[0] + ' features selected')
        # add these geomorphology attribute fields
        fields = arcpy.ListFields(inFeatClass)
        field_names = [f.name for f in fields]
        # a list of attributes to be added and calculated
        fieldList = ['PhysiogSetting','GeomorphSetting','Basic_Geom_Unit','BGU_T','BGU_sT','ProcessAttribute',
                     'GeometricAttribute','Grouping','Age','StratPosition','SeaLevel','Lithology','GrainSize',
                     'TerrianAttributes','ProcessClass','AeolianInput','Comments','GeomorphAnalystName',
                     'GeomorphAnalystOrganisation']
        for fieldName in fieldList:
            fieldType = "TEXT"
            fieldLength = 200
            if fieldName in field_names:
                arcpy.AddMessage(fieldName + " already exists and will be calculated/recalculated")
            else:
                arcpy.AddField_management(inFeatClass,fieldName,fieldType,field_length=fieldLength)
                arcpy.AddMessage(fieldName + " added")


        # calculate fields
        # must be done on the active layer on ArcGIS Pro Map. Otherwise, the selection wonot be honoured
        i = 0
        for field in fieldList:
            # calculate string to a text field, the string must be enclosed by double quote
            expression = '"' + valueList[i] + '"'
            arcpy.CalculateField_management(lyr, field, expression, "PYTHON_9.3")
            i += 1

        arcpy.AddMessage("all fields calculated")
        
  

        return


# define helper functions here
class helpers(object):
    # This function converts backslach (accepted through the ArcGIS tool) to forwardslach (needed in python script) in a path
    def convert_backslash_forwardslash(self,inText):
        # inText: input path
        
        inText = fr"{inText}"
        if inText.find('\t'):
            inText = inText.replace('\t', '\\t')
        elif inText.find('\n'):
            inText = inText.replace('\n', '\\n')
        elif inText.find('\r'):
            inText = inText.replace('\r', '\\r')

        inText = inText.replace('\\','/')
        return inText

    def is_number(self,n):
        is_number = True
        try:
            num = float(n)
            # check for "nan" floats
            is_number = num == num   # or use `math.isnan(num)`
        except ValueError:
            is_number = False
        return is_number

    def do_current_induced(self,parameters):                
        if parameters[4].value:
            if parameters[4].value == 'bedform':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['scour','current-induced furrow','obstacle and comet scour',
                                             'cyclic step','dune','sediment wave','sediment ridge','megaripple',
                                             'ripple','plane bed','sediment streak','sediment ribbon','lineation',
                                             'current-induced crag and tail','lag'])
            elif parameters[4].value == 'barform':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['pointbar','counterpoint bar','scroll bar','mid-channel bar',
                                             'bank-attached','riffle (and pool)','ledge','bench','levee','mouthbar',
                                             'crevasse splay'])
            else:
                parameters[5].filter.list = ['NA','Unknown']

        if parameters[5].value:
            if parameters[5].value == 'cyclic step':
                parameters[6].filter.list = ['NA','Unknown','aggradational','non-aggradational']
            elif parameters[5].value in ['dune','sediment wave','sediment ridge','megaripple']:
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['foredune','coastal dune','linear','transverse','star',
                                             'barchan','trochoidal','lunette','dome','antidune','parabolic','nebkha',
                                             'lee','climbing','blowout','jökulhlaup dunes',
                                             'small (0.075 – 0.4 m (height) / 0.6 – 5.0 m (wavelength))',
                                             'medium (0.4 – 0.75 m (height) / 5 - 10 m (wavelength))',
                                             'large (0.75 – 5.0 m (height) / 10 – 100 m (wavelength))',
                                             'very large (>5 m (height) / >100 m (wavelength))'])
            else:
                parameters[6].filter.list = ['NA','Unknown']

        return

    def do_coastal(self,parameters):
        if parameters[4].value:
            if parameters[4].value == 'coastal subaerial valley':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['coastal incised valley','ria','coastal fjord'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'floodplain terrace':
                parameters[5].filter.list = ['NA','Unknown','strath']
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'floodplain':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['high-energy confined floodplain',
                                             'medium-energy unconfined floodplain',
                                             'low-energy cohesive floodplain'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value in ['coastal delta','delta lobe']:
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['upper','lower','coastal delta-front','coastal pro-delta',
                                             'bayhead','shelf edge','tidal delta'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'subaerial channel':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['river','creek','distributary','gully','rill','tidal inlet'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value in ['barrier complex','barrier system']:
                parameters[5].filter.list = ['NA','Unknown','chenier plain','strandplain']
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'barrier':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['salient/tombolo','bay-mouth barrier','barrier spit',
                                             'barrier island'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'tidal flat':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['supratidal flat','subtidal flat','intertidal flat'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'lagoon':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['closed lagoon','open lagoon',
                                             'intermittently closed and open lagoon'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value in ['beach','raised beach']:
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['reflective','dissipative','intermediate',
                                             'reef or rock affected beach'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'rocky coast':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['outcrop','plunging cliff','cliff','toe (rocky coast)',
                                             'shore platform','notch','stack','arch','pool','lapies','marine karren',
                                             'cave','ramp','pothole','furrow (rocky coast)','rampart'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'coastal barform':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['nearshore bar','berm','shoreface terrace',
                                             'intertidal terrace','marine terrace','beach cusp','crescentic bar',
                                             'ridge and runnel','washover bar','intertidal bar','ridgebar','tidal bar'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'bedform':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['scour','current-induced furrow','obstacle and comet scour',
                                             'cyclic step','dune','sediment wave','sediment ridge','megaripple',
                                             'ripple','plane bed','sediment streak','sediment ribbon','lineation',
                                             'current-induced crag and tail','lag'])
                parameters[7].filter.list = ['NA'] + sorted(['erosional','accretionary/aggradational','unidirectional flow',
                                             'bidirectional flow','interference','constrained flow','open flow',
                                             'tidal current','turbidity current','density current'])
                parameters[8].filter.list = ['NA'] + sorted(['2D','3D','primary','secondary','compound','longitudinal',
                                             'transverse','oblique','straight crests','sinuous crests',
                                             'linguoid crests','lunate crests','crescent'])
            elif parameters[4].value == 'barform':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['pointbar','counterpoint bar','scroll bar','mid-channel bar',
                                             'bank-attached','riffle (and pool)','ledge','bench','levee','mouthbar',
                                             'crevasse splay'])
                parameters[7].filter.list = ['NA'] + sorted(['erosional','accretionary/aggradational','unidirectional flow',
                                             'bidirectional flow','interference','constrained flow','open flow',
                                             'tidal current','turbidity current','density current'])
                parameters[8].filter.list = ['NA'] + sorted(['2D','3D','primary','secondary','compound','longitudinal',
                                             'transverse','oblique','straight crests','sinuous crests',
                                             'linguoid crests','lunate crests','crescent'])
            elif parameters[4].value in ['current-induced channel','chute channel','oxbow','plunge pool','knickpoint']:
                parameters[5].filter.list = ['NA','Unknown']
                parameters[7].filter.list = ['NA'] + sorted(['erosional','accretionary/aggradational','unidirectional flow',
                                             'bidirectional flow','interference','constrained flow','open flow',
                                             'tidal current','turbidity current','density current'])
                parameters[8].filter.list = ['NA'] + sorted(['2D','3D','primary','secondary','compound','longitudinal',
                                             'transverse','oblique','straight crests','sinuous crests',
                                             'linguoid crests','lunate crests','crescent'])
            else:
                parameters[5].filter.list = ['NA','Unknown']
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
        if parameters[5].value:
            if parameters[5].value == 'coastal incised valley':
                parameters[6].filter.list = ['NA','Unknown','coastal plain','cross-shelf']
            elif parameters[5].value in ['river','creek','distributary']:
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['straight','meandering','braided','anabranching'])
            elif parameters[5].value == 'barrier spit':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['flying','continuation','baymouth','recurved','cuspate',
                                             'foreland'])
            elif parameters[5].value == 'cyclic step':
                parameters[6].filter.list = ['NA','Unknown','aggradational','non-aggradational']
            elif parameters[5].value in ['dune','sediment wave','sediment ridge','megaripple']:
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['foredune','coastal dune','linear','transverse','star',
                                             'barchan','trochoidal','lunette','dome','antidune','parabolic','nebkha',
                                             'lee','climbing','blowout','jökulhlaup dunes',
                                             'small (0.075 – 0.4 m (height) / 0.6 – 5.0 m (wavelength))',
                                             'medium (0.4 – 0.75 m (height) / 5 - 10 m (wavelength))',
                                             'large (0.75 – 5.0 m (height) / 10 – 100 m (wavelength))',
                                             'very large (>5 m (height) / >100 m (wavelength))'])
            else:
                parameters[6].filter.list = ['NA','Unknown']

        return

    def do_fluvial(self,parameters):
        if parameters[4].value:
            if parameters[4].value == 'drainage network':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['dendritic','parallel','radial','centrifugal',
                                             'centripetal','distributary','angular','trellis','annular'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'fluvial subaerial valley':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['fluvial incised valley','river valley'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'floodplain terrace':
                parameters[5].filter.list = ['NA', 'Unknown', 'strath']
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'floodplain':
                parameters[5].filter.list = ['NA', 'Unknown'] + sorted(['high-energy confined floodplain',
                                             'medium-energy unconfined floodplain',
                                             'low-energy cohesive floodplain'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value in ['fluvial delta','delta lobe']:
                parameters[5].filter.list = ['NA','Unknown','fluvial delta-front','fluvial pro-delta']
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'subaerial channel':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['river','creek','distributary','gully','rill','tidal inlet'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'bedform':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['scour','current-induced furrow','obstacle and comet scour',
                                             'cyclic step','dune','sediment wave','sediment ridge','megaripple',
                                             'ripple','plane bed','sediment streak','sediment ribbon','lineation',
                                             'current-induced crag and tail','lag'])
                parameters[7].filter.list = ['NA'] + sorted(['erosional','accretionary/aggradational','unidirectional flow',
                                             'bidirectional flow','interference','constrained flow','open flow',
                                             'tidal current','turbidity current','density current'])
                parameters[8].filter.list = ['NA'] + sorted(['2D','3D','primary','secondary','compound','longitudinal',
                                             'transverse','oblique','straight crests','sinuous crests',
                                             'linguoid crests','lunate crests','crescent'])
            elif parameters[4].value == 'barform':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['pointbar','counterpoint bar','scroll bar','mid-channel bar',
                                             'bank-attached','riffle (and pool)','ledge','bench','levee','mouthbar',
                                             'crevasse splay'])
                parameters[7].filter.list = ['NA'] + sorted(['erosional','accretionary/aggradational','unidirectional flow',
                                             'bidirectional flow','interference','constrained flow','open flow',
                                             'tidal current','turbidity current','density current'])
                parameters[8].filter.list = ['NA'] + sorted(['2D','3D','primary','secondary','compound','longitudinal',
                                             'transverse','oblique','straight crests','sinuous crests',
                                             'linguoid crests','lunate crests','crescent'])
            elif parameters[4].value in ['current-induced channel','chute channel','oxbow','plunge pool','knickpoint']:
                parameters[5].filter.list = ['NA','Unknown']
                parameters[7].filter.list = ['NA'] + sorted(['erosional','accretionary/aggradational','unidirectional flow',
                                             'bidirectional flow','interference','constrained flow','open flow',
                                             'tidal current','turbidity current','density current'])
                parameters[8].filter.list = ['NA'] + sorted(['2D','3D','primary','secondary','compound','longitudinal',
                                             'transverse','oblique','straight crests','sinuous crests',
                                             'linguoid crests','lunate crests','crescent'])
            else:
                parameters[5].filter.list = ['NA','Unknown']
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
        if parameters[5].value:
            if parameters[5].value == 'cyclic step':
                parameters[6].filter.list = ['NA','Unknown','aggradational','non-aggradational']
            elif parameters[5].value in ['dune','sediment wave','sediment ridge','megaripple']:
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['foredune','coastal dune','linear','transverse','star',
                                             'barchan','trochoidal','lunette','dome','antidune','parabolic','nebkha',
                                             'lee','climbing','blowout','jökulhlaup dunes',
                                             'small (0.075 – 0.4 m (height) / 0.6 – 5.0 m (wavelength))',
                                             'medium (0.4 – 0.75 m (height) / 5 - 10 m (wavelength))',
                                             'large (0.75 – 5.0 m (height) / 10 – 100 m (wavelength))',
                                             'very large (>5 m (height) / >100 m (wavelength))'])
            else:
                parameters[6].filter.list = ['NA','Unknown']

        return

    def do_marine(self,parameters):
        if parameters[4].value:
            if parameters[4].value == 'marine barform':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['sediment apron','sediment lobe','sediment drift',
                                             'contourite drift','sediment bank','sediment ridge'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value in ['submarine canyon','submarine tributary canyon']:
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['self-incising canyon','slope-confined canyon',
                                             'blind canyon'])
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'bedform':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['scour','current-induced furrow','obstacle and comet scour',
                                             'cyclic step','dune','sediment wave','sediment ridge','megaripple',
                                             'ripple','plane bed','sediment streak','sediment ribbon','lineation',
                                             'current-induced crag and tail','lag'])
                parameters[7].filter.list = ['NA'] + sorted(['erosional','accretionary/aggradational','unidirectional flow',
                                             'bidirectional flow','interference','constrained flow','open flow',
                                             'tidal current','turbidity current','density current'])
                parameters[8].filter.list = ['NA'] + sorted(['2D','3D','primary','secondary','compound','longitudinal',
                                             'transverse','oblique','straight crests','sinuous crests',
                                             'linguoid crests','lunate crests','crescent'])
            elif parameters[4].value == 'barform':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['pointbar','counterpoint bar','scroll bar','mid-channel bar',
                                             'bank-attached','riffle (and pool)','ledge','bench','levee','mouthbar',
                                             'crevasse splay'])
                parameters[7].filter.list = ['NA'] + sorted(['erosional','accretionary/aggradational','unidirectional flow',
                                             'bidirectional flow','interference','constrained flow','open flow',
                                             'tidal current','turbidity current','density current'])
                parameters[8].filter.list = ['NA'] + sorted(['2D','3D','primary','secondary','compound','longitudinal',
                                             'transverse','oblique','straight crests','sinuous crests',
                                             'linguoid crests','lunate crests','crescent'])
            elif parameters[4].value in ['current-induced channel','chute channel','oxbow','plunge pool','knickpoint']:
                parameters[5].filter.list = ['NA','Unknown']
                parameters[7].filter.list = ['NA'] + sorted(['erosional','accretionary/aggradational','unidirectional flow',
                                             'bidirectional flow','interference','constrained flow','open flow',
                                             'tidal current','turbidity current','density current'])
                parameters[8].filter.list = ['NA'] + sorted(['2D','3D','primary','secondary','compound','longitudinal',
                                             'transverse','oblique','straight crests','sinuous crests',
                                             'linguoid crests','lunate crests','crescent'])
            else:
                parameters[5].filter.list = ['NA','Unknown']
                parameters[7].filter.list = ['NA']
                parameters[8].filter.list = ['NA']
        if parameters[5].value:
            if parameters[5].value in ['sediment bank','sediment ridge']:
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['banner','headland','sinuosoidal','linear'])
            elif parameters[5].value == 'cyclic step':
                parameters[6].filter.list = ['NA','Unknown','aggradational','non-aggradational']
            elif parameters[5].value in ['dune','sediment wave','sediment ridge','megaripple']:
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['foredune','coastal dune','linear','transverse','star',
                                             'barchan','trochoidal','lunette','dome','antidune','parabolic','nebkha',
                                             'lee','climbing','blowout','jökulhlaup dunes',
                                             'small (0.075 – 0.4 m (height) / 0.6 – 5.0 m (wavelength))',
                                             'medium (0.4 – 0.75 m (height) / 5 - 10 m (wavelength))',
                                             'large (0.75 – 5.0 m (height) / 10 – 100 m (wavelength))',
                                             'very large (>5 m (height) / >100 m (wavelength))'])
            else:
                parameters[6].filter.list = ['NA','Unknown']

        return

    def do_glacial(self,parameters):
        if parameters[4].value:
            if parameters[4].value in ['U-shaped valley','cross-shelf trough']:
                parameters[5].filter.list = ['NA','Unknown','hanging valley','valley/trough head']
            elif parameters[4].value == 'streamlined landform':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['roche moutonnée','whaleback','glacial crag and tail',
                                             'mega-scale glacial lineation','bundle structure',
                                             'drumlin','flute','groove'])
            elif parameters[4].value == 'hill-hole pair':
                parameters[5].filter.list = ['NA','Unknown','glacitectonic hill','glacitectonic hole']
            elif parameters[4].value == 'moraine':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['recessional moraine','lateral moraine',
                                             'shear-margin moraine','push moraine','terminal moraine','De Geer moraine'])
            elif parameters[4].value == 'iceberg ploughmark':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['single-keeled ploughmark','multi-keeled ploughmark'])
            else:
                parameters[5].filter.list = ['NA','Unknown']
        if parameters[5].value:
            if parameters[5].value == 'drumlin':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['sediment drumlin','sediment drumlin with rock-core',
                                             'rock drumlin'])
            elif parameters[5].value == 'flute':
                parameters[6].filter.list = ['NA','Unknown','megaflute']
            elif parameters[5].value == 'groove':
                parameters[6].filter.list = ['NA','Unknown','megagroove']
            else:
                parameters[6].filter.list = ['NA','Unknown']

        return

    def do_solidEarth(self,parameters):
        if parameters[4].value:
            if parameters[4].value == 'volcano (island or submarine)':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['seamount','shield volcano','stratovolcano'])
            elif parameters[4].value == 'bedrock outcrop (undefined)':
                parameters[5].filter.list = ['NA','Unknown','bedded','foliated','massive']
            elif parameters[4].value == 'magmatic outcrop':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['circular volcanic depression','volcanic fissure',
                                             'volcanic plateau','magmatic dome','magmatic sheet',
                                             'volcanic plug/neck','volcanic flow'])
            elif parameters[4].value == 'tectonic depression':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['tectonic basin','graben','half graben','fault valley'])
            elif parameters[4].value == 'tectonic high':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['solid earth compressional ridge','tectonic dome','horst',
                                             'back-tilted fault block'])
            elif parameters[4].value == 'bedding ridge':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['cuesta','homoclinal ridge','hogback'])
            elif parameters[4].value in ['tectonic lineament','tectonic escarpment']:
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['fault','joint','fracture zone'])
            else:
                parameters[5].filter.list = ['NA','Unknown']
        if parameters[5].value:
            if parameters[5].value == 'circular volcanic depression':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['collapse caldera','drainage caldera','pit crater',
                                             'lava rise pit','explosion crater'])
            elif parameters[5].value == 'volcanic plateau':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['lava plateau','inflation plateau','lava mesa'])
            elif parameters[5].value == 'magmatic dome':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['pluton','batholith','laccolith','lava dome'])
            elif parameters[5].value == 'magmatic sheet':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['dyke','sill','lopolith'])
            elif parameters[5].value == 'volcanic flow':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['lava flow (channellised, hummocky, sheet, pillow, blocks)',
                                             'pressure ridge','flow lobe'])
            elif parameters[5].value == 'tectonic basin':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['piggyback basin','sag basin','pull-apart basin','synform',
                                             'shutter basin'])
            elif parameters[5].value == 'solid earth compressional ridge':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['thrust ridge','pressure ridge','shutter ridge'])
            elif parameters[5].value == 'tectonic dome':
                parameters[6].filter.list = ['NA','Unknown','antiform','diapir dome']
            else:
                parameters[6].filter.list = ['NA','Unknown']

        return

    def do_biogenic(self,parameters):
        if parameters[4].value:
            if parameters[4].value == 'biogenic reef':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['cold-water-coral-reef','coralligène','bank','rim',
                                             'patch reef','fringing reef','barrier reef','atoll','platform reef',
                                             'juvenile: unmodified antecedent platform',
                                             'submerged','irregular mature: crescentic','lagoonal senile: planar'])
            elif parameters[4].value in ['fore-reef','reef crest','reef flat','back reef','reef lagoon',
                                         'spur-and-groove']:
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['patch reef','fringing reef',
                                             'barrier reef','atoll','platform reef',
                                             'juvenile: unmodified antecedent platform',
                                             'submerged','irregular mature: crescentic','lagoonal senile: planar'])
            elif parameters[4].value == 'biostrome':
                parameters[5].filter.list = ['NA','Unknown','ribbon','sheet']
            elif parameters[4].value in ['bioherm','mound']:
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['lenticular','reticulate','annulate/annular',
                                             'agglutinating'])
            elif parameters[4].value == 'mat':
                parameters[5].filter.list = ['NA','Unknown','aggregation','sediment trapped/bound']
            elif parameters[4].value == 'bed':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['ribbon','sheet','aggregation','sediment trapped/bound'])
            elif parameters[4].value == 'excavation':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['feeding trace','nest','burrow','boring','resting site',
                                             'track','trail','mound'])
            else:
                parameters[5].filter.list = ['NA','Unknown']
        if parameters[5].value:
            if parameters[5].value in ['cold-water-coral-reef','coralligène','bank','rim','patch reef','fringing reef',
                                       'barrier reef','atoll','platform reef',
                                       'juvenile: unmodified antecedent platform','submerged',
                                       'irregular mature: crescentic','lagoonal senile: planar','ribbon','sheet',
                                       'lenticular','reticulate','annulate/annular']:
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['cold-water-corals','coralline (red) algae','bryozoa',
                                             'foraminifera','vermetid','serpulid','bivalve','brachiopod','sponge',
                                             'hermatypic corals','calcareous (green) algae',
                                             'undefined bioconstructor (any BGU or BGU-T)','rhodolith (maerl)',
                                             'microbial','micritic','peloidal','stromatolite'])
            elif parameters[5].value == 'agglutinating':
                parameters[6].filter.list = ['NA','Unknown','polychaete (e.g., Sabellaria)']
            elif parameters[5].value in ['aggregation','sediment trapped/bound']:
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['siliceous sponge','echinoderm','seagrass',
                                             'fleshy/filamentous algae','mangrove'])
            else:
                parameters[6].filter.list = ['NA','Unknown']

        return

    def do_massMovement(self,parameters):
        if parameters[4].value:
            if parameters[4].value == 'fall':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['rock fall','debris fall'])
            elif parameters[4].value == 'topple':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['rock topple','debris topple'])
            elif parameters[4].value == 'slide':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['translational slide','rotational slide','slump',
                                             'frontally confined slide','frontally emergent slide'])
            elif parameters[4].value == 'flow':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['rock avalanche','debris flow','mudflow','turbidity current'])
            elif parameters[4].value == 'translated block':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['detached block','rafted block','outrunner block'])
            else:
                parameters[5].filter.list = ['NA','Unknown']
        if parameters[5].value:
            parameters[6].filter.list = ['NA','Unknown']

        return

    def do_fluidFlow(self,parameters):
        if parameters[4].value:
            if parameters[4].value == 'mud volcano':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['mud dome','cone','mud pie'])
                parameters[8].filter.list = ['NA']                
            elif parameters[4].value == 'outcropping methane-derived authigenic carbonate (MDAC)':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['MDAC slab','MDAC chimney','MDAC pavements','MDAC mounds'])
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'pockmark':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['unit pockmark','normal pockmark','giant pockmark',
                                             'complex pockmark','strings of pockmarks'])
                parameters[8].filter.list = ['NA'] + sorted(['asymmetric','symmetric','circular','elliptical','elongated',
                                             'eyed','U-shaped','V-shaped','W-shaped'])
            elif parameters[4].value == 'hydrothermal vent':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['white smokers','black smokers'])
                parameters[8].filter.list = ['NA']
            elif parameters[4].value == 'pingo':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['permafrost pingo','gas hydrate pingo','gas hydrate mound'])
                parameters[8].filter.list = ['NA']
            else:
                parameters[5].filter.list = ['NA','Unknown']
                parameters[8].filter.list = ['NA']
        if parameters[5].value:
            parameters[6].filter.list = ['NA','Unknown']

        return

    def do_karst(self,parameters):
        if parameters[4].value:
            if parameters[4].value == 'carbonate karst':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['cone karst','tower karst','karst plain','spring',
                                             'blind valley','carbonate doline'])
            elif parameters[4].value == 'salt karst':
                parameters[5].filter.list = ['NA','Unknown','salt doline']
            elif parameters[4].value == 'sandstone karst':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['sandstone doline','ruiniform'])
            else:
                parameters[5].filter.list = ['NA','Unknown']
        if parameters[5].value:
            if parameters[5].value == 'carbonate doline':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['dissolution','collapse','uvala','polje','blue hole'])
            else:
                parameters[6].filter.list = ['NA','Unknown']

        return

    def do_anthropogenic(self,parameters):
        if parameters[4].value:
            if parameters[4].value == 'archaeological':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['cultural site','historical wreck','other archaeological'])
            elif parameters[4].value == 'structure':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['artificial reef','fish farm','fish trap','pipeline',
                                             'foundations and moorings','coastal management structure',
                                             'rubbish discharge','debris','cable','mine','other structure','wreck'])
            elif parameters[4].value == 'disturbance':
                parameters[5].filter.list = ['NA','Unknown'] + sorted(['mine tailings','dredge spoil','bottom trawl',
                                             'dredge scour','anchor drag','other disturbance'])
            else:
                parameters[5].filter.list = ['NA','Unknown']
        if parameters[5].value:
            if parameters[5].value == 'pipeline':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['diffuser','wellhead','outfall','intake'])
            elif parameters[5].value == 'foundations and moorings':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['pillars','anchors','moorings'])
            elif parameters[5].value == 'coastal management structure':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['jetty','groyne','pontoon','breakwall'])
            elif parameters[5].value == 'wreck':
                parameters[6].filter.list = ['NA','Unknown'] + sorted(['ship','plane','other (e.g. car)'])
            else:
                parameters[6].filter.list = ['NA','Unknown']

        return
