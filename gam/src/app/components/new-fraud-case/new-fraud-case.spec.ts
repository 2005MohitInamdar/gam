import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewFraudCase } from './new-fraud-case';

describe('NewFraudCase', () => {
  let component: NewFraudCase;
  let fixture: ComponentFixture<NewFraudCase>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewFraudCase],
    }).compileComponents();

    fixture = TestBed.createComponent(NewFraudCase);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
