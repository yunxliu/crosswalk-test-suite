Feature: css3-fonts
 Scenario: font 014
   When launch "css3-fonts-app"
     And I go to "csswg/font-014.htm"
     And I save the page to "font-014"
    Then pic "font-014" of baseline and result should be "100" similar if have results
