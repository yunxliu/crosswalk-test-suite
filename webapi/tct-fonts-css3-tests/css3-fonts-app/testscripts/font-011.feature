Feature: css3-fonts
 Scenario: font 011
   When launch "css3-fonts-app"
     And I go to "csswg/font-011.htm"
     And I save the page to "font-011"
    Then pic "font-011" of baseline and result should be "100" similar if have results
