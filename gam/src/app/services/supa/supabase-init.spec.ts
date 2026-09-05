import { TestBed } from '@angular/core/testing';

import { SupabaseInit } from './supabase-init';

describe('SupabaseInit', () => {
  let service: SupabaseInit;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SupabaseInit);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
