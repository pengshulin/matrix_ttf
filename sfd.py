#!/usr/bin/env python
# coding:utf-8
'''
sfd file used for FontForge
'''
import fontforge, pygame
import time, os, pprint

pygame.init()


class Sfd:
    def __init__( self, filename=None ):
        self.filename = filename
        if filename != None and os.path.isfile( filename ):
            self.sfdfile = fontforge.open( filename )
        else:
            self.sfdfile = fontforge.font()
            # set default
            self.setName( 'unnamed' )
            self.sfdfile.weight = 'Medium'
            self.sfdfile.copyright =  \
                   'Created with python-fontforge, edit with FontForge'
            self.sfdfile.comment = 'Created %s'% time.ctime()
            self.sfdfile.ascent = 1000
            self.sfdfile.descent = 0
            self.sfdfile.upos = 0
            self.sfdfile.encoding = 'UnicodeFull'
        self.glyphs = {}
 
    def setName( self, name ):
        self.sfdfile.fontname = name
        self.sfdfile.fullname = name 
        self.sfdfile.familyname = name 

    def setCopyright( self, description ):
        self.sfdfile.copyright = description
        
    def addGlyphs( self, fontname, height, bold, unichars ):
        font = pygame.font.Font( fontname, height )
        font.set_bold(bold)
        for uc in unichars:
            if not self.glyphs.has_key( uc ):
                #print ord(uc), uc, fontname, height, bold
                img = font.render( uc, False, (0, 0, 0), (255, 255, 255) )
                self.glyphs[uc] = img

    def printGlyphs( self ):
        pprint.pprint( self.glyphs )

    def mergeGlyphs( self ):
        # merge self.glyphs to self.sfdfile
        print 'glyphs number:', len(self.glyphs)
        if not len(self.glyphs):
            return
        # calc max graph size
        minwidth, minheight, maxwidth, maxheight = 100000, 100000, 0, 0
        for uc in list(self.glyphs):
            w, h = self.glyphs[uc].get_size()
            #print 'u%d(%d,%d)'%(ord(c),w,h),
            print '%s(%d,%d)'% (uc, w, h),
            if w < minwidth:
                minwidth = w 
            if w > maxwidth:
                maxwidth = w 
            if h < minheight:
                minheight = h
            if h > maxheight:
                maxheight = h
        print ''
        print 'glyph size: width(%d ~ %d), height(%d ~ %d)'%\
                 (minwidth, maxwidth, minheight, maxheight )
        delta = abs( self.sfdfile.ascent - self.sfdfile.descent ) / maxheight
        new_font_height = delta * maxheight
        print 'adjust font height to: %d'%new_font_height
        self.sfdfile.ascent = self.sfdfile.descent + new_font_height

        # add glyphs
        def drawPixelOnGlyph( glyph, x, y, height ):
            pen = glyph.glyphPen(replace=False)
            x0, x1 = delta*x, delta*(x+1)
            # bottom aligned area
            y0 = self.sfdfile.descent + delta*(height-1-y)
            y1 = self.sfdfile.descent + delta*((height-1-y)+1)
            # move up if necessary
            dy = (maxheight - height) / 2 
            y0 += delta * dy
            y1 += delta * dy
            # draw rectangle
            pen.moveTo((x0, y0))
            pen.lineTo((x1, y0))
            pen.lineTo((x1, y1))
            pen.lineTo((x0, y1))
            pen.closePath()
            pen = None
        
        # add glyph 
        for c in list(self.glyphs):
            g = self.glyphs[c]
            width, height = g.get_size()
            glyph = self.sfdfile.createChar(ord(c))
            glyph.width = width * delta
            for y in range(height):
                for x in range(width):
                    if g.get_at((x,y))[0] == 0:
                        drawPixelOnGlyph( glyph, x, y, height )
            glyph.removeOverlap()
            glyph.simplify()

    def save( self, filename=None ):
        if filename:
            self.filename = filename
        self.sfdfile.save( self.filename )

    def exportTtf( self, ttfname ):
        self.sfdfile.generate( ttfname ) 
 
if __name__ == '__main__':
    # test
    SFD = Sfd()
    #SFD.add_glyphs( 'tahomabd.ttf', 13, False, [unicode(chr(i)) for i in range(32, 127)] )
    SFD.addGlyphs( 'arialbd.ttf', 13, False, [unicode(chr(i)) for i in range(32, 127)] )
    SFD.addGlyphs( 'simsun.ttc', 15, False, [u'中', u'文', u'测', u'试'] )
    SFD.printGlyphs()
    SFD.mergeGlyphs()
    SFD.save('test.sfd')
    SFD.exportTtf( 'test.ttf' )


