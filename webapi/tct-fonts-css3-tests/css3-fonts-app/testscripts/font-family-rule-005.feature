Feature: css3-fonts
 Scenario: font family rule 005
   When launch "css3-fonts-app"
     And I go to "csswg/font-family-rule-005.htm"
     And I save the page to "font-family-rule-005"
    Then pic "font-family-rule-005" of baseline and result should be "100" similar if have results
