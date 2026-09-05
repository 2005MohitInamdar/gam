import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class NewCaseData {
  // Replaces @Input() isOpen + @Output() closeModal
  private _isModalOpen = new BehaviorSubject<boolean>(false);
  isModalOpen$ = this._isModalOpen.asObservable();

  openModal(): void {
    this._isModalOpen.next(true);
  }

  closeModal(): void {
    this._isModalOpen.next(false);
  }
}
