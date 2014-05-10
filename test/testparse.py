"""
Author: Sean Sill
File: TestParser
"""

import pixapi
import logging
import testutils

#Make this into a formal test script 
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_input = TEST_INPUT.encode('utf-8')
    render = pixapi.PixRender(test_input)
    im = render.render_image()
    testutils.SimpleShow(im)
    
    # Next test