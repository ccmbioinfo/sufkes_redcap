import sys
from Check import Check

def checkRequiredFields(req_vars, indep_vars, row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map, err_thres=0.65):
    row = records[row_index]

#    element_bad = False

    num_missing = 0
    num_checked = 0

    for req_var in req_vars:
        displayed_by_bl = False
        if (metadata[req_var].branching_logic == None):
            diplayed_by_bl = True
        elif metadata[req_var].branching_logic(row_index, form_repetition_map, records, record_id_map):
            displayed_by_bl = True
        if displayed_by_bl:
            num_checked += 1
            if (metadata[req_var].field_type == "checkbox"):
                checkbox_empty = True
                for checkbox in metadata[req_var].choices:
                    if (row[checkbox] == "1"):
                        checkbox_empty = False 
                        break
                if (checkbox_empty):
#                    element_bad = True ##
                    num_missing += 1
#                    break
            else:
                if (row[req_var] == ""):
#                    element_bad = True ##
                    num_missing += 1
#                    break

    for indep_var, dep_var_list in indep_vars.iteritems():
        dep_var_list_has_empties = False
        if (row[indep_var] == "1"): # assume independent variable is a single checkbox whose dependent variables should be completed if the box is checked.
            num_checked += 1
            for dep_var in dep_var_list:
                dep_var_empty = True
                for option in dep_var:
                    # is current option empty?
                    if (metadata[option].field_type == "checkbox"):
                        if (row[option] == "1"):
                            dep_var_empty = False
                            break
                    else:
                        if (row[option] != ""):
                            dep_var_empty = False
                            break
                if dep_var_empty:
                    dep_var_list_has_empties = True
                    break # Stop looking if one of the dep vars is empty.
        if dep_var_list_has_empties:
#            element_bad = True
            num_missing += 1
#            break

    completion_rate = 1.0 - float(num_missing)/float(num_checked)
    print completion_rate
    if (completion_rate > err_thres):
        element_bad = True
    else:
        element_bad = False
    return element_bad


# Create list of checks (must be called 'checklist')
checklist = []


######## CSVT SUBFORM ########

#### Check: Records for which the question 'Will the CSVT subform be submitted?' is displayed by branching logic, and 'Yes' is selected.
name = "csvt_subform_level_1"
description = "Records for which the question 'Will the CSVT subform be submitted?' is displayed by branching logic, and 'Yes' is selected."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["csvtgrp"] # first field should lie in the field, event, instance which you would like to be reported.

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    return True

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    if (row["csvtgrp"] == "1"):
        element_bad = True
    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction

#### Check: Records for which at least one of the highest-level fields in the CSVT subform (those which are always displayed when the subform is being completed) are filled in.
name = "csvt_subform_level_2"
description = "Records for which at least one of the highest-level fields in the CSVT subform (those which are always displayed when the subform is being completed) are filled in."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]#["anemia", "aprothro", "ldisea___1", "lupus___1", "renaldis___1", "hthrom", "mdiab___1", "othcondu___1", "othcosp", "vinstass___1", "vinstass___2", "vinstass___3", "comdel___1", "posthem___1", "placeret", "respdis", "mecasp", "csvtasym", "irrita___1", "cnp___1", "papill___1", "chencep___1", "neofeed___1", "neofeed___2", "neofeed___3", "noproth___1", "apcr", "apcrval", "apcrdate", "at3", "at3val", "at3unit", "at3date", "aptt", "apttval", "apttunit", "apttdate", "fac8", "fac8val", "fac8unit", "fac8date", "fibrin", "fibrval", "fibrunit", "fibrdate", "homocy", "homoval", "homounit", "homodate", "inr", "inrval", "inrdate", "ddim", "ddimval", "ddimunit", "ddimdate", "lipo", "lipoval", "lipodate", "lupan", "lupval", "lupdate", "plasm", "plasval", "plasunit", "plasdate", "prst", "prstval", "prstunit", "prstdate", "prsf", "prsfval", "prsfunit", "prsfdate", "prc", "prcval", "prcunit", "prcdate", "thrt", "thrtval", "thrtdate", "fac5", "fac5date", "mthfr", "mtfrdate", "gene", "genedate", "acla", "aclaval", "acladate", "ctspec___1", "ctspec___2", "ctspec___3", "mrispec___1", "mrispec___2", "mrispec___3", "mrispec___4", "mrispec___5", "csvtloca___1", "csvtloca___2", "csvtloca___3", "medstart", "medend", "medint", "meddur", "recanst", "csvtint", "csvtradi", "csvtrelo", "rcsvinfn", "rhemloc___1", "rhemloc___2", "rhemloc___3"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["csvtgrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    fields_to_check = ["anemia", "aprothro", "ldisea___1", "lupus___1", "renaldis___1", "hthrom", "mdiab___1", "othcondu___1", "othcosp", "vinstass___1", "vinstass___2", "vinstass___3", "comdel___1", "posthem___1", "placeret", "respdis", "mecasp", "csvtasym", "irrita___1", "cnp___1", "papill___1", "chencep___1", "neofeed___1", "neofeed___2", "neofeed___3", "noproth___1", "apcr", "apcrval", "apcrdate", "at3", "at3val", "at3unit", "at3date", "aptt", "apttval", "apttunit", "apttdate", "fac8", "fac8val", "fac8unit", "fac8date", "fibrin", "fibrval", "fibrunit", "fibrdate", "homocy", "homoval", "homounit", "homodate", "inr", "inrval", "inrdate", "ddim", "ddimval", "ddimunit", "ddimdate", "lipo", "lipoval", "lipodate", "lupan", "lupval", "lupdate", "plasm", "plasval", "plasunit", "plasdate", "prst", "prstval", "prstunit", "prstdate", "prsf", "prsfval", "prsfunit", "prsfdate", "prc", "prcval", "prcunit", "prcdate", "thrt", "thrtval", "thrtdate", "fac5", "fac5date", "mthfr", "mtfrdate", "gene", "genedate", "acla", "aclaval", "acladate", "ctspec___1", "ctspec___2", "ctspec___3", "mrispec___1", "mrispec___2", "mrispec___3", "mrispec___4", "mrispec___5", "csvtloca___1", "csvtloca___2", "csvtloca___3", "medstart", "medend", "medint", "meddur", "recanst", "csvtint", "csvtradi", "csvtrelo", "rcsvinfn", "rhemloc___1", "rhemloc___2", "rhemloc___3"]

    for field_name in fields_to_check:
        if (metadata[field_name].field_type == "checkbox"):
            if (row[field_name] == "1"):
                element_bad = True
                break
        else:
            if (row[field_name] != ""):
                element_bad = True
                break
    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction

#### Check: CSVT subform complete - level 2
name = "csvt_subform_level_3"
description = "Patients who completed the entire CSVT subform except possibly free text and date fields."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["csvtgrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False ##

    row = records[row_index]

    req_vars = ["anemia", "aprothro", "hthrom", "placeret", "respdis", "mecasp", "csvtasym", "apcr", "apcrval", "at3", "at3val", "at3unit", "aptt", "apttval", "apttunit", "fac8", "fac8val", "fac8unit", "fibrin", "fibrval", "fibrunit", "homocy", "homoval", "homounit", "inr", "inrval", "ddim", "ddimval", "ddimunit", "lipo", "lipoval", "lupan", "lupval", "plasm", "plasval", "plasunit", "prst", "prstval", "prstunit", "prsf", "prsfval", "prsfunit", "prc", "prcval", "prcunit", "thrt", "thrtval", "fac5", "mthfr", "gene", "acla", "aclaval", "ctspec___1", "mrispec___1", "csvtloca___1", "meddur", "recanst", "csvtint", "csvtradi", "csvtrelo", "rcsvtloc___0", "rcsvtlsp___1", "rcsvttsp___1", "supfotsp", "rcsvinfn", "rhemloc___1"]

    indep_vars = {}

    element_bad = checkRequiredFields(req_vars, indep_vars, row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map)

    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction


######## PERINATAL SUBFORM ########

#### Check: Records for which the question 'Will the perinatal subform be submitted?' is displayed by branching logic, and 'Yes' is selected.
name = "perinatal_subform_level_1"
description = "Records for which the question 'Will the perinatal subform be submitted?' is displayed by branching logic, and 'Yes' is selected."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["perigrp"] # first field should lie in the field, event, instance which you would like to be reported.

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    return True

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    if (row["perigrp"] == "1"):
        element_bad = True
    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction


#### Check: Records for which at least one of the highest-level fields in the perinatal subform (those which are always displayed when the subform is being completed) are filled in.
name = "perinatal_subform_level_2"
description = "Records for which at least one of the highest-level fields in the perinatal subform (those which are always displayed when the subform is being completed) are filled in."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]#["heainjsp", "neohie___1", "bilrubin___1", "histepil", "hdevdel", "hcerpal", "hblclot", "hthrom", "cosang", "nprepreg", "nchild", "sponabor", "nmedterm", "infert", "medconpr___1", "medconpr___2", "medconpr___3", "medconpr___4", "medconpr___5", "medconpr___6", "medconpr___7", "medconpr___8", "medconpr___9", "medconpr___10", "medconpr___11", "medconpr___12", "medconpr___13", "medconpr___14", "medconpr___15", "medconpr___16", "medvita___1", "medvita___2", "medvita___3", "vityes", "illdrug", "concep", "medcondu___1", "medcondu___2", "medcondu___3", "medcondu___4", "medcondu___5", "medcondu___6", "medcondu___7", "medcondu___8", "medcondu___9", "medcondu___10", "medcondu___11", "medcondu___12", "medcondu___13", "medcondu___14", "medcondu___15", "medcondu___16", "medcondu___17", "medcondu___18", "medcondu___19", "medcondu___20", "medcondu___21", "medcondu___22", "medcondu___23", "medcondu___24", "medcondu___25", "medcondu___26", "medcondu___27", "medcondu___28", "medcondu___29", "medcondu___30", "medcondu___31", "mdiab___1", "othcondu___1", "othcosp", "alcpreg", "smokpreg", "drugpreg", "naus___1", "phyinjdu___1", "toxchem___1", "freqactd", "decfeta", "obstda___1", "obstda___2", "obstda___3", "gbsstat", "cesarsp", "pcesar", "vsponind", "vinstass___1", "vinstass___2", "vinstass___3", "comdel___1", "oxysyn___1", "secstag___1", "posthem___1", "placeret", "placeabn", "placpath", "pathrep", "heacirc", "shdysto___1", "fepedyst___1", "fetmon___1", "fetmon___2", "fetmon___3", "fetmon___4", "fetmon___5", "fetmon___6", "fetmon___7", "resus", "umbcor___1", "cordneck", "neocath", "intub", "respdis", "exchtran", "mecon", "mecasp", "modefeed___1", "modefeed___2", "modefeed___3", "modefeed___4", "subfed___1", "subfed___2", "subfed___3", "subfed___4", "convuls___1", "convuls___2", "neurconc___1", "neurconc___2", "neurconc___3", "neurconc___4", "neurconc___5", "neurconc___6", "neurconc___7", "neurconc___8", "irrita___1", "gradconc", "armweak___1", "legweak___1", "hyperto___1", "hypoto___1", "tortico___1", "movdis___1", "landelsp___1", "landelsp___2", "behavabn___1", "cogabn___1", "failthr___1", "respdif___1", "neofeed___1", "neofeed___2", "neofeed___3", "handfist___1", "earhapre___1", "absen___1", "compar___1", "infansp___1", "othrseiz___1", "seizind", "seizinde", "numseiz", "statep", "statepi", "statepsp___1", "statepsp___2", "eegyes", "noproth___1", "apcr", "apcrval", "apcrdate", "at3", "at3val", "at3unit", "at3date", "aptt", "apttval", "apttunit", "apttdate", "fac8", "fac8val", "fac8unit", "fac8date", "fibrin", "fibrval", "fibrunit", "fibrdate", "homocy", "homoval", "homounit", "homodate", "inr", "inrval", "inrdate", "ddim", "ddimval", "ddimunit", "ddimdate", "lipo", "lipoval", "lipodate", "lupan", "lupval", "lupdate", "plasm", "plasval", "plasunit", "plasdate", "prst", "prstval", "prstunit", "prstdate", "prsf", "prsfval", "prsfunit", "prsfdate", "prc", "prcval", "prcunit", "prcdate", "thrt", "thrtval", "thrtdate", "fac5", "fac5date", "mthfr", "mtfrdate", "gene", "genedate", "acla", "aclaval", "acladate", "numanti", "anti1", "ant1al", "anti2", "ant2al", "anti3", "ant3al", "anti4", "ant4al", "anti5", "ant5al"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["perigrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    fields_to_check = ["heainjsp", "neohie___1", "bilrubin___1", "histepil", "hdevdel", "hcerpal", "hblclot", "hthrom", "cosang", "nprepreg", "nchild", "sponabor", "nmedterm", "infert", "medconpr___1", "medconpr___2", "medconpr___3", "medconpr___4", "medconpr___5", "medconpr___6", "medconpr___7", "medconpr___8", "medconpr___9", "medconpr___10", "medconpr___11", "medconpr___12", "medconpr___13", "medconpr___14", "medconpr___15", "medconpr___16", "medvita___1", "medvita___2", "medvita___3", "vityes", "illdrug", "concep", "medcondu___1", "medcondu___2", "medcondu___3", "medcondu___4", "medcondu___5", "medcondu___6", "medcondu___7", "medcondu___8", "medcondu___9", "medcondu___10", "medcondu___11", "medcondu___12", "medcondu___13", "medcondu___14", "medcondu___15", "medcondu___16", "medcondu___17", "medcondu___18", "medcondu___19", "medcondu___20", "medcondu___21", "medcondu___22", "medcondu___23", "medcondu___24", "medcondu___25", "medcondu___26", "medcondu___27", "medcondu___28", "medcondu___29", "medcondu___30", "medcondu___31", "mdiab___1", "othcondu___1", "othcosp", "alcpreg", "smokpreg", "drugpreg", "naus___1", "phyinjdu___1", "toxchem___1", "freqactd", "decfeta", "obstda___1", "obstda___2", "obstda___3", "gbsstat", "cesarsp", "pcesar", "vsponind", "vinstass___1", "vinstass___2", "vinstass___3", "comdel___1", "oxysyn___1", "secstag___1", "posthem___1", "placeret", "placeabn", "placpath", "pathrep", "heacirc", "shdysto___1", "fepedyst___1", "fetmon___1", "fetmon___2", "fetmon___3", "fetmon___4", "fetmon___5", "fetmon___6", "fetmon___7", "resus", "umbcor___1", "cordneck", "neocath", "intub", "respdis", "exchtran", "mecon", "mecasp", "modefeed___1", "modefeed___2", "modefeed___3", "modefeed___4", "subfed___1", "subfed___2", "subfed___3", "subfed___4", "convuls___1", "convuls___2", "neurconc___1", "neurconc___2", "neurconc___3", "neurconc___4", "neurconc___5", "neurconc___6", "neurconc___7", "neurconc___8", "irrita___1", "gradconc", "armweak___1", "legweak___1", "hyperto___1", "hypoto___1", "tortico___1", "movdis___1", "landelsp___1", "landelsp___2", "behavabn___1", "cogabn___1", "failthr___1", "respdif___1", "neofeed___1", "neofeed___2", "neofeed___3", "handfist___1", "earhapre___1", "absen___1", "compar___1", "infansp___1", "othrseiz___1", "seizind", "seizinde", "numseiz", "statep", "statepi", "statepsp___1", "statepsp___2", "eegyes", "noproth___1", "apcr", "apcrval", "apcrdate", "at3", "at3val", "at3unit", "at3date", "aptt", "apttval", "apttunit", "apttdate", "fac8", "fac8val", "fac8unit", "fac8date", "fibrin", "fibrval", "fibrunit", "fibrdate", "homocy", "homoval", "homounit", "homodate", "inr", "inrval", "inrdate", "ddim", "ddimval", "ddimunit", "ddimdate", "lipo", "lipoval", "lipodate", "lupan", "lupval", "lupdate", "plasm", "plasval", "plasunit", "plasdate", "prst", "prstval", "prstunit", "prstdate", "prsf", "prsfval", "prsfunit", "prsfdate", "prc", "prcval", "prcunit", "prcdate", "thrt", "thrtval", "thrtdate", "fac5", "fac5date", "mthfr", "mtfrdate", "gene", "genedate", "acla", "aclaval", "acladate", "numanti", "anti1", "ant1al", "anti2", "ant2al", "anti3", "ant3al", "anti4", "ant4al", "anti5", "ant5al"]

    for field_name in fields_to_check:
        if (metadata[field_name].field_type == "checkbox"):
            if (row[field_name] == "1"):
                element_bad = True
                break
        else:
            if (row[field_name] != ""):
                element_bad = True
                break
    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction

#### Check: Perinatal subform complete - level 2
name = "perinatal_subform_level_3"
description = "Patients who completed the entire perinatal subform except possibly free text and date fields."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["perigrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False ##

    row = records[row_index]

    req_vars = ["neohiegr", "histepil", "hdevdel", "hcerpal", "hblclot", "hthrom", "cosang", "nprepreg", "nchild", "sponabor", "nmedterm", "infert", "illdrug", "concep", "alcpreg", "smokpreg", "drugpreg", "freqactd", "decfeta", "obstda___1", "gbsstat", "cesarsp", "pcesar", "vsponind", "placeret", "placeabn", "placcosp___1", "placpath", "heacirc", "resus", "resussp___1", "cordneck", "neocath", "ncathty___1", "intub", "respdis", "exchtran", "mecon", "mecasp", "modefeed___1", "subfed___1", "neurconc___1", "gradconc", "aweaksp___1", "lweaksp___1", "hypersp___1", "hyposp___1", "hfistsp", "seizind", "seizinde", "numseiz", "statep", "eegyes", "eegtype___1", "eegres", "eegepil", "elecseiz", "elseizsp___1", "epildisc", "epilsp___1", "focside___1", "mfocside___1", "genside___1", "genslo", "genslow___1", "apcr", "apcrval", "at3", "at3val", "at3unit", "aptt", "apttval", "apttunit", "fac8", "fac8val", "fac8unit", "fibrin", "fibrval", "fibrunit", "homocy", "homoval", "homounit", "inr", "inrval", "ddim", "ddimval", "ddimunit", "lipo", "lipoval", "lupan", "lupval", "plasm", "plasval", "plasunit", "prst", "prstval", "prstunit", "prsf", "prsfval", "prsfunit", "prc", "prcval", "prcunit", "thrt", "thrtval", "fac5", "fac5date", "mthfr", "gene", "acla", "aclaval", "numanti", "anti1", "ant1al", "anti2", "ant2al", "anti3", "ant3al", "anti4", "ant4al", "anti5", "ant5al"]

    indep_vars = {}

    element_bad = checkRequiredFields(req_vars, indep_vars, row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map)

    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction



######## ARTERIOPATHY SUBFORM ########

#### Check: Records for which the question 'Will the arteriopathy subfom be submitted?' is displayed by branching logic, and 'Yes' is selected.
name = "arteriopathy_subfform_level_1"
description = "Records for which the question 'Will the arteriopathy subform be submitted?' is displayed by branching logic, and 'Yes' is selected."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["artegrp"] # first field should lie in the field, event, instance which you would like to be reported.

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    return True

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    if (row["artegrp"] == "1"):
        element_bad = True
    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction

#### Check: Records for which at least one of the highest-level fields in the arteriopathy subform (those which are always displayed when the subform is being completed) are filled in. Do not include arteriopathy subform fields in the follow-up event.
name = "arteriopathy_subform_level_2"
description = "Records for which at least one of the highest-level fields in the arteriopathy subform (those which are always displayed when the subform is being completed) are filled in. Do not include arteriopathy subform-fields in the follow-up event."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]#["artdate", "artmajor", "tcaothsp", "artsecsp___1", "artsecsp___2", "artsecsp___3", "artsecsp___4", "artsecsp___5", "artsecsp___6", "artsecsp___7", "artsecsp___8", "artsecde", "stutonse", "initcoll", "colluncl", "collscan", "initpseu", "pseuuncl", "pseuscan", "initroto", "roocuncl", "roocscan"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["artegrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    fields_to_check = ["artdate", "artmajor", "tcaothsp", "artsecsp___1", "artsecsp___2", "artsecsp___3", "artsecsp___4", "artsecsp___5", "artsecsp___6", "artsecsp___7", "artsecsp___8", "artsecde", "stutonse", "initcoll", "colluncl", "collscan", "initpseu", "pseuuncl", "pseuscan", "initroto", "roocuncl", "roocscan"]

    for field_name in fields_to_check:
        if (metadata[field_name].field_type == "checkbox"):
            if (row[field_name] == "1"):
                element_bad = True
                break
        else:
            if (row[field_name] != ""):
                element_bad = True
                break
    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction

#### Check: Arteriopathy subform complete - level 2
name = "arteriopathy_subform_level_3"
description = "Patients who completed the entire arteriopathy subform except possibly free text and date fields."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["artegrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False ##

    row = records[row_index]

    req_vars = ["artmajor", "artsmall", "artfca", "tcahigh", "tcawhy___1", "dishigh", "diswhy___1", "thromhi", "thromwh___1", "bca", "aoart", "artsecsp___1", "stutonse", "initcoll", "collscan", "initpseu", "pseuscan", "initroto", "roocscan"]

    indep_vars = {}

    element_bad = checkRequiredFields(req_vars, indep_vars, row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map)

    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction



######## SEIZURE SUBFORM ########

#### Check: Records for which the question 'Will the seizure subform be submitted?' is displayed by branching logic, and 'Yes' is selected.
name = "seiz_subform_level_1"
description = "Records for which the question 'Will the seizure subform be submitted?' is displayed by branching logic, and 'Yes' is selected."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["seizgrp"] # first field should lie in the field, event, instance which you would like to be reported.

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    return True

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    if (row["seizgrp"] == "1"):
        element_bad = True
    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction

#### Check: Records for which at least one of the highest-level fields in the seizure subform (those which are always displayed when the subform is being completed) are filled in.
name = "seiz_subform_level_2"
description = "Records for which at least one of the highest-level fields in the seizure subform (those which are always displayed when the subform is being completed) are filled in."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]#["absen___1", "compar___1", "infansp___1", "othrseiz___1", "seizind", "seizinde", "numseiz", "statep", "statepi", "statepsp___1", "statepsp___2", "eegyes", "numanti", "anti1", "ant1al", "anti2", "ant2al", "anti3", "ant3al", "anti4", "ant4al", "anti5", "ant5al"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["seizgrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    fields_to_check = ["absen___1", "compar___1", "infansp___1", "othrseiz___1", "seizind", "seizinde", "numseiz", "statep", "statepi", "statepsp___1", "statepsp___2", "eegyes", "numanti", "anti1", "ant1al", "anti2", "ant2al", "anti3", "ant3al", "anti4", "ant4al", "anti5", "ant5al"]

    for field_name in fields_to_check:
        if (metadata[field_name].field_type == "checkbox"):
            if (row[field_name] == "1"):
                element_bad = True
                break
        else:
            if (row[field_name] != ""):
                element_bad = True
                break
    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction

#### Check: Seizure subform complete - level 2
name = "seiz_subform_level_3"
description = "Patients who completed the entire seizure subform except possibly free text and date fields."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["seizgrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False ##

    row = records[row_index]

    req_vars = ["seizind", "seizinde", "numseiz", "statep", "statepi", "statepsp___1", "eegyes", "eegtype___1", "prorechr", "eegres", "eegepil", "elecseiz", "elseizsp___1", "epildisc", "epilsp___1", "focside___1", "mfocside___1", "genside___1", "genslo", "genslow___1", "numanti", "anti1", "ant1al", "anti2", "ant2al", "anti3", "ant3al", "anti4", "ant4al", "anti5", "ant5al"]

    indep_vars = {}

    element_bad = checkRequiredFields(req_vars, indep_vars, row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map)

    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction



######## CARDIAC SUBFORM ########

#### Check: Records for which the question 'Will the cardiac subform be submitted?' is displayed by branching logic, and 'Yes' is selected.
name = "card_subform_level_1"
description = "Records for which the question 'Will the cardiac subform be submitted?' is displayed by branching logic, and 'Yes' is selected."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["cardgrp"] # first field should lie in the field, event, instance which you would like to be reported.

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    return True

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    if (row["cardgrp"] == "1"):
        element_bad = True
    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction


#### Check: Records for which at least one of the highest-level fields in the cardiac subform (those which are always displayed when the subform is being completed) are filled in.
name = "card_subform_level_2"
description = "Records for which at least one of the highest-level fields in the cardiac subform (those which are always displayed when the subform is being completed) are filled in."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]#["chdspec___1", "chdspec___2", "chdspec___3", "chdspec___4", "chdspec___5", "chdspec___6", "chdspec___7", "chdspec___8", "chdspec___9", "chdspec___10", "chdspec___11", "chdspec___12", "chdspec___13", "chdspec___14", "chdspec___15", "chdspec___16", "chdspec___17", "chdspec___18", "chdspec___19", "chdspec___20", "chdspec___21", "chdspec___22", "chdspec___23", "valdis___1", "libsack___1", "cardmy___1", "arryth___1", "kawas___1", "myocard___1", "inttum___1", "rejtrans___1", "ahdoth___1", "aneury___1", "hetr___1", "hetr___2", "pulartera___1", "pulartera___2", "blatauss___1", "blatauss___2", "snomonor___1", "snomonor___2", "norwoo___1", "norwoo___2", "glenn___1", "glenn___2", "fontan___1", "fontan___2", "artswit___1", "artswit___2", "artswwi___1", "artswwi___2", "ross___1", "ross___2", "kono___1", "kono___2", "truart___1", "truart___2", "fallot___1", "fallot___2", "tapvc___1", "tapvc___2", "avcan___1", "avcan___2", "valvu___1", "valvu___2", "melod___1", "melod___2", "valrep___1", "valrep___2", "asd___1", "asd___2", "vsdclos___1", "vsdclos___2", "surgoth___1", "surgoth___2", "surgreop", "bypass", "crclam", "trans", "ballo___1", "ballo___2", "stent___1", "stent___2", "ablat___1", "ablat___2", "devpl___1", "devpl___2", "balldil___1", "balldil___2", "thromb___1", "thromb___2", "othdev___1", "othdev___2", "rcathlis", "eclscan", "eclsart", "eclsed", "vadt___1", "vadt___2", "vadt___3", "vadt___4", "vadt___5", "vadt___6", "vaded", "proriais___1", "proriais___2", "proriais___3", "proriais___4", "proriais___5", "proriais___6", "proriais___7", "proriais___8", "proriais___9", "o2sat", "echejfr", "ejfrsp___1", "ejfrsp___2", "ejfrsp___3", "ejfrsp___4", "ejfrsp___5", "ejfrsp___6", "ejfrsp___7", "ejfrsp___8", "ejfrsp___9", "cardrf___1", "cardrf___2", "cardrf___3", "cardrf___4", "cardrf___5", "echoef", "echot___1", "echot___2", "ekg", "holter", "tcd", "othte"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["cardgrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    fields_to_check = ["chdspec___1", "chdspec___2", "chdspec___3", "chdspec___4", "chdspec___5", "chdspec___6", "chdspec___7", "chdspec___8", "chdspec___9", "chdspec___10", "chdspec___11", "chdspec___12", "chdspec___13", "chdspec___14", "chdspec___15", "chdspec___16", "chdspec___17", "chdspec___18", "chdspec___19", "chdspec___20", "chdspec___21", "chdspec___22", "chdspec___23", "valdis___1", "libsack___1", "cardmy___1", "arryth___1", "kawas___1", "myocard___1", "inttum___1", "rejtrans___1", "ahdoth___1", "aneury___1", "hetr___1", "hetr___2", "pulartera___1", "pulartera___2", "blatauss___1", "blatauss___2", "snomonor___1", "snomonor___2", "norwoo___1", "norwoo___2", "glenn___1", "glenn___2", "fontan___1", "fontan___2", "artswit___1", "artswit___2", "artswwi___1", "artswwi___2", "ross___1", "ross___2", "kono___1", "kono___2", "truart___1", "truart___2", "fallot___1", "fallot___2", "tapvc___1", "tapvc___2", "avcan___1", "avcan___2", "valvu___1", "valvu___2", "melod___1", "melod___2", "valrep___1", "valrep___2", "asd___1", "asd___2", "vsdclos___1", "vsdclos___2", "surgoth___1", "surgoth___2", "surgreop", "bypass", "crclam", "trans", "ballo___1", "ballo___2", "stent___1", "stent___2", "ablat___1", "ablat___2", "devpl___1", "devpl___2", "balldil___1", "balldil___2", "thromb___1", "thromb___2", "othdev___1", "othdev___2", "rcathlis", "eclscan", "eclsart", "eclsed", "vadt___1", "vadt___2", "vadt___3", "vadt___4", "vadt___5", "vadt___6", "vaded", "proriais___1", "proriais___2", "proriais___3", "proriais___4", "proriais___5", "proriais___6", "proriais___7", "proriais___8", "proriais___9", "o2sat", "echejfr", "ejfrsp___1", "ejfrsp___2", "ejfrsp___3", "ejfrsp___4", "ejfrsp___5", "ejfrsp___6", "ejfrsp___7", "ejfrsp___8", "ejfrsp___9", "cardrf___1", "cardrf___2", "cardrf___3", "cardrf___4", "cardrf___5", "echoef", "echot___1", "echot___2", "ekg", "holter", "tcd", "othte"]

    for field_name in fields_to_check:
        if (metadata[field_name].field_type == "checkbox"):
            if (row[field_name] == "1"):
                element_bad = True
                break
        else:
            if (row[field_name] != ""):
                element_bad = True
                break
    return element_bad

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction

#### Check: Cardiac subform complete - level 2
name = "card_subform_level_3"
description = "Patients who completed the entire cardiac subform except possibly free text and date fields."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["cardgrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]

    req_vars = ["chdspec___1", "valdispe___1", "valinv___1", "cardmysp___1", "arrytsp___1", "inttumsp___1", "valrept", "devplt", "eclsart", "vadt___1", "echoef", "echot___1", "tte___1", "tee___1", "ekg", "ekgres", "ekgabn___1", "holter", "holterre", "holtabn___1", "tcd", "tcdsp___1", "othte"]
    
    indep_vars = {} # dict mapping independent variables (e.g. Congential heart disease) in the subform to dependent variables (e.g. type of congenital heart disease)
    # Check that at least one of each dependent variable is filled in for each independent variable.

    indep_vars["ahd___1"] = [["infcard___1", "valdis___1", "libsack___1", "cardmy___1", "arryth___1", "kawas___1", "myocard___1", "inttum___1", "rejtrans___1", "ahdoth___1"]]
    indep_vars["csurg___1"] = [["hetr___1", "hetr___2", "pulartera___1", "pulartera___2", "blatauss___1", "blatauss___2", "snomonor___1",  "snomonor___2", "norwoo___1", "norwoo___2", "glenn___1", "glenn___2", "fontan___1", "fontan___2", "artswit___1", "artswit___2", "artswwi___1", "artswwi___2", "ross___1", "ross___2", "kono___1", "kono___2", "truart___1", "truart___2", "fallot___1", "fallot___2", "tapvc___1", "tapvc___2", "avcan___1", "avcan___2", "valvu___1", "valvu___2", "melod___1", "melod___2", "valrep___1", "valrep___2", "asd___1", "asd___2", "vsdclos___1", "vsdclos___2", "surgoth___1", "surgoth___2"], ["surgreop"]]
    indep_vars["carcath___1"] = [["ballo___1", "ballo___2", "stent___1", "stent___2", "ablat___1", "ablat___2", "devpl___1", "devpl___2", "balldil___1", "balldil___2", "thromb___1", "thromb___2", "othdev___1", "othdev___2"]]

    element_bad = checkRequiredFields(req_vars, indep_vars, row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map)

    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction



######## tPA SUBFORM ########

#### Check: Records for which the question 'Will the tPA subform be submitted?' is displayed by branching logic, and 'Yes' is selected.
name = "tpa_subform_level_1"
description = "Records for which the question 'Will the tPA subform be submitted?' is displayed by branching logic, and 'Yes' is selected."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["tpagrp"] # first field should lie in the field, event, instance which you would like to be reported.

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    return True

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    if (row["tpagrp"] == "1"):
        element_bad = True
    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction


#### Check: Records for which at least one of the highest-level fields in the tPA subform (those which are always displayed when the subform is being completed) are filled in.
name = "tpa_subform_level_2"
description = "Records for which at least one of the highest-level fields in the tPA subform (those which are always displayed when the subform is being completed) are filled in."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["tpagrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False

    row = records[row_index]
    
    fields_to_check = ["chickmo", "chickye", "diab", "neckinj", "immunal___1", "immunal___2", "commig", "migaura", "seizmh", "epilmh", "dehydr", "cohemp", "cohempsp", "handed", "papill___1", "landelsp___1", "landelsp___2", "statep", "noproth___1", "apcr", "apcrval", "apcrdate", "at3", "at3val", "at3unit", "at3date", "aptt", "apttval", "apttunit", "apttdate", "fac8", "fac8val", "fac8unit", "fac8date", "fibrin", "fibrval", "fibrunit", "fibrdate", "homocy", "homoval", "homounit", "homodate", "inr", "inrval", "inrdate", "ddim", "ddimval", "ddimunit", "ddimdate", "lipo", "lipoval", "lipodate", "lupan", "lupval", "lupdate", "plasm", "plasval", "plasunit", "plasdate", "prst", "prstval", "prstunit", "prstdate", "prsf", "prsfval", "prsfunit", "prsfdate", "prc", "prcval", "prcunit", "prcdate", "thrt", "thrtval", "thrtdate", "fac5", "fac5date", "mthfr", "mtfrdate", "gene", "genedate", "acla", "aclaval", "acladate", "tpadose", "tpabolus", "tpatimfi", "tpacaths", "tpainjst", "tpainjen", "tpamicro", "tpacathwi", "tpadescr", "hemeva___1", "ivd___1", "vps___1", "aceta___1", "immsup___1", "oxsup___1", "transfus___1", "transfus___3", "transfus___4", "transfus___5", "asploc___1", "asploc___2", "asprhem___1", "asprhem___2", "asprhem___3", "asprhem___4", "asprhem___5", "asprhem___6", "asprhem___7", "asprhem___8", "asprhem___9", "asprhem___10", "asprhem___11", "asprhem___12", "asprhem___13", "asprhem___14", "asprhem___15", "asplhem___1", "asplhem___2", "asplhem___3", "asplhem___4", "asplhem___5", "asplhem___6", "asplhem___7", "asplhem___8", "asplhem___9", "asplhem___10", "asplhem___11", "asplhem___12", "asplhem___13", "asplhem___14", "asplhem___15", "asppfoss___1", "asppfoss___2", "asppfoss___3", "asppfoss___4", "asppfoss___5", "vasabnon___1", "vasabnon___2", "vasabnon___3", "tpaica___1", "tpaica___2", "tpaaca___1", "tpaaca___2", "tpaprmca___1", "tpaprmca___2", "tpadimca___1", "tpadimca___2", "tpalento___1", "tpalento___2", "tpapca___1", "tpapca___2", "tpavb___1", "tpavb___2", "addnfind___1", "addnfind___2", "addnfind___3", "addnfind___4", "addnfind___5", "addnfind___6", "pretbpda", "pretbpti", "pretbpsy", "pretbpdi", "p30tbpti", "p30tbpsy", "p30tbpdi", "p12tbpti", "p12tbpsy", "p12tbpdi", "p12mbpda", "p12mbpti", "p12mbpsy", "p12mbpdi", "postctda", "postctti", "postmrid", "postmrit", "parenchf", "vasculaf", "intcrahe", "pasploc___1", "pasploc___2", "pasprhem___1", "pasprhem___2", "pasprhem___3", "pasprhem___4", "pasprhem___5", "pasprhem___6", "pasprhem___7", "pasprhem___8", "pasprhem___9", "pasprhem___10", "pasprhem___11", "pasprhem___12", "pasprhem___13", "pasprhem___14", "pasprhem___15", "pasplhem___1", "pasplhem___2", "pasplhem___3", "pasplhem___4", "pasplhem___5", "pasplhem___6", "pasplhem___7", "pasplhem___8", "pasplhem___9", "pasplhem___10", "pasplhem___11", "pasplhem___12", "pasplhem___13", "pasplhem___14", "pasplhem___15", "pasppfos___1", "pasppfos___2", "pasppfos___3", "pasppfos___4", "pasppfos___5", "ae", "abnproth"]

    for field_name in fields_to_check:
        if (metadata[field_name].field_type == "checkbox"):
            if (row[field_name] == "1"):
                element_bad = True
                break
        else:
            if (row[field_name] != ""):
                element_bad = True
                break
    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction

#### Check: tPA subform complete - level 2
name = "tpa_subform_level_3"
description = "Patients who completed the entire tPA subform except possibly free text and date fields."
report_forms = False
inter_project = False
whole_row_check = False
check_invalid_entries = False
inter_record = False
inter_row = False
specify_fields = True
target_fields = ["ipssid"]

def rowConditions(row_index, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    check_row = False
    if (records[row_index]["tpagrp"] == "1"):
        check_row = True
    return check_row

fieldConditions = None

def checkFunction(row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map):
    element_bad = False ##

    row = records[row_index]

    req_vars = ["chickmo", "chickye", "diab", "diabsp", "neckinj", "commig", "migaura", "seizmh", "epilmh", "dehydr", "cohemp", "handed", "statep", "statepi", "apcr", "apcrval", "at3", "at3val", "at3unit", "aptt", "apttval", "apttunit", "fac8", "fac8val", "fac8unit", "fibrin", "fibrval", "fibrunit", "homocy", "homoval", "homounit", "inr", "inrval", "ddim", "ddimval", "ddimunit", "lipo", "lipoval", "lupan", "lupval", "plasm", "plasval", "plasunit", "prst", "prstval", "prstunit", "prsf", "prsfval", "prsfunit", "prc", "prcval", "prcunit", "thrt", "thrtval", "fac5", "mthfr", "gene", "acla", "aclaval", "tpadose", "tpabolus", "tpabolam", "tpamicro", "transfus___1", "asploc___1", "asprhem___1", "asplhem___1", "asppfoss___1", "vasabnon___1", "tpaica___1", "tpaaca___1", "tpaprmca___1", "tpadimca___1", "tpalento___1", "tpapca___1", "tpavb___1", "pretbpsy", "pretbpdi", "p30tbpsy", "p30tbpdi", "p12tbpsy", "p12tbpdi", "p12mbpsy", "p12mbpdi", "pedniy", "pednisc", "preloc", "prelocq", "prelocc", "pregaze", "previs", "prefac", "prerarm", "prelarm", "prerleg", "prelleg", "prelim", "prelimra", "prelimla", "prelimrl", "prelimll", "presens", "prelang", "predys", "preext", "pednis", "posloc", "poslocq", "poslocc", "posgaze", "posvis", "posfac", "posrarm", "poslarm", "posrleg", "poslleg", "poslim", "possens", "poslang", "posdys", "posext", "pednist", "parenchf", "vasculaf", "intcrahe", "hemworse", "parenlat___1", "pasploc___1", "pasprhem___1", "pasplhem___1", "pasppfos___1", "ae", "aenum", "ae1type", "ae1sev", "ae1rel", "ae1acti___1", "ae1ser", "ae1outc", "ae2type", "ae2sev", "ae2rel", "ae2acti___1", "ae2ser", "ae2outc", "ae3type", "ae3sev", "ae3rel", "ae3acti___1", "ae3ser", "ae3outc", "ae4type", "ae4sev", "ae4rel", "ae4acti___1", "ae4ser", "ae4outc", "ae5type", "ae5sev", "ae5rel", "ae5acti___1", "ae5ser", "ae5outc", "ae6type", "ae6sev", "ae6rel", "ae6acti___1", "ae6ser", "ae6outc", "ae7type", "ae7sev", "ae7rel", "ae7acti___1", "ae7ser", "ae7outc", "ae8type", "ae8sev", "ae8rel", "ae8acti___1", "ae8ser", "ae8outc", "ae9type", "ae9sev", "ae9rel", "ae9acti___1", "ae9ser", "ae9outc", "ae10type", "ae10sev", "ae10rel", "ae10acti___1", "ae10ser", "ae10outc", "ae11type", "ae11sev", "ae11rel", "ae11acti___1", "ae11ser", "ae11outc", "ae12type", "ae12sev", "ae12rel", "ae12acti___1", "ae12ser", "ae12outc"]

    indep_vars = {}

    element_bad = checkRequiredFields(req_vars, indep_vars, row_index, field_name, def_field, metadata, records, record_id_map, repeating_forms_events, form_repetition_map)

    return element_bad 

#print "************************SKIPPING CHECK '"+name+"' FOR TEST************************"
checklist.append(Check(name, description, report_forms, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction))
del name, description, inter_project, whole_row_check, check_invalid_entries, inter_record, inter_row, specify_fields, target_fields, rowConditions, fieldConditions, checkFunction
