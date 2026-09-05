import { TestBed } from '@angular/core/testing';

import { NewCaseData } from './new-case-data';

describe('NewCaseData', () => {
  let service: NewCaseData;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NewCaseData);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
