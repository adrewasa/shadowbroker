# uncompyle6 version 2.9.10
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.0b2 (default, Oct 11 2016, 05:27:10) 
# [GCC 6.2.0 20161005]
# Embedded file name: Mcl_Cmd_Activity_DataHandler.py


def DataHandlerMain(namespace, InputFilename, OutputFilename):
    import mcl.imports
    import mcl.data.Input
    import mcl.data.Output
    import mcl.status
    import mcl.target
    import mcl.object.Message
    mcl.imports.ImportNamesWithNamespace(namespace, 'mca.status.cmd.activity', globals())
    input = mcl.data.Input.GetInput(InputFilename)
    output = mcl.data.Output.StartOutput(OutputFilename, input)
    output.Start('Activity', 'activity', [])
    msg = mcl.object.Message.DemarshalMessage(input.GetData())
    if input.GetStatus() != mcl.status.MCL_SUCCESS:
        errorMsg = msg.FindMessage(mcl.object.Message.MSG_KEY_RESULT_ERROR)
        moduleError = errorMsg.FindU32(mcl.object.Message.MSG_KEY_RESULT_ERROR_MODULE)
        osError = errorMsg.FindU32(mcl.object.Message.MSG_KEY_RESULT_ERROR_OS)
        output.RecordModuleError(moduleError, osError, errorStrings)
        output.EndWithStatus(input.GetStatus())
        return True
    else:
        if msg.GetCount() == 0:
            output.EndWithStatus(mcl.target.CALL_SUCCEEDED)
            return True
        results = Result()
        results.Demarshal(msg)
        if results.moreData and results.lastActivity.GetTimeType() == results.lastActivity.MCL_TIME_TYPE_NOT_A_TIME:
            output.GoToBackground()
        from mcl.object.XmlOutput import XmlOutput
        xml = XmlOutput()
        if results.moreData:
            xml.Start('NewActivity')
        else:
            xml.Start('Activity')
        xml.AddTimeElement('Last', results.lastActivity)
        output.RecordXml(xml)
        if results.moreData:
            output.End()
            return True
        output.EndWithStatus(mcl.target.CALL_SUCCEEDED)
        return True


if __name__ == '__main__':
    import sys
    try:
        namespace, InputFilename, OutputFilename = sys.argv[1:]
    except:
        print '%s <namespace> <input filename> <output filename>' % sys.argv[0]
        sys.exit(1)

    if DataHandlerMain(namespace, InputFilename, OutputFilename) != True:
        sys.exit(-1)