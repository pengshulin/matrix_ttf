#!/usr/bin/env python
# encoding:utf-8
'''
generate matrix ttf font used for UI prototyping design
'''
import sfd, pprint, os

__copyright__ = 'Matrix TTF, designed by Peng Shulin <trees_peng@163.com>'

LIST_ASCII = [unicode(chr(i)) for i in range(32, 127)]
LIST_LATIN = [(chr(i)+'\x00').decode('utf-16') for i in \
                 list(range(0x0020,0x007f) + range(0x00a1,0x0100))]
 
CONFIG = {}

for h in range(9,50):
    cfg = { 'height': h, 'bold': False, 'chars': LIST_LATIN }
    cfg_bold = { 'height': h, 'bold': True, 'chars': LIST_LATIN }

    #CONFIG['matrix_tahomabd_%d_latin'% h] = {'tahomabd.ttf': cfg }
    #CONFIG['matrix_tahoma_%d_latin'% h] = {'tahoma.ttf': cfg }
    #CONFIG['matrix_arialbd_%d_latin'% h] = {'arialbd.ttf': cfg }
    #CONFIG['matrix_arial_%d_latin'% h] = {'arial.ttf': cfg }
    CONFIG['matrix_dejavusansbd_%d_latin'% h] = {'DejaVuSans-Bold.ttf': cfg }
    CONFIG['matrix_dejavusans_%d_latin'% h] = {'DejaVuSans.ttf': cfg }


#pprint.pprint( CONFIG )
                
if not os.path.isdir( 'matrix_ttf' ):
    os.mkdir( 'matrix_ttf' )
for fname in CONFIG:
    SFD = sfd.Sfd()
    SFD.setName( fname )
    SFD.setCopyright( __copyright__ )
    for ttfname in CONFIG[fname]:
        cfg = CONFIG[fname][ttfname]
        SFD.addGlyphs( ttfname, cfg['height'], cfg['bold'], cfg['chars'] )
    SFD.mergeGlyphs()
    SFD.exportTtf( 'matrix_ttf/%s.ttf'%fname )
    del SFD

